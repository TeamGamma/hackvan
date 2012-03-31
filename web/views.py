from flask import render_template, request, session, flash, url_for, redirect
from web import app
import settings
from web.database import db
from web.models import (
    Player, Game
)

import twilio.twiml
from twilio.rest import TwilioRestClient

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html', settings=settings)

# TODO: add support for flash messages and fake twilio requests
@app.route('/textmessage', methods=['GET', 'POST'])
def fake_message():
    """
    Web interface for faking text messages.
    """
    # Mark this user as a web interface user
    session['user_type'] = 'web'

    # Form submission
    if request.method == 'POST':
        app.logger.debug(repr(dict(request.form)))
        phone = request.form['phone']
        message = request.form['message']

        # Call the main text message handler
        response = handle_player_text(phone, message)

        # Persist all changes to the database
        db.session.commit()

        if response:
            flash(response)

        return redirect(url_for('fake_message'))
    else:
        # Show text message form
        return render_template('text_message.html', settings=settings)


@app.route("/sms", methods=['POST'])
def twilio_message():
    """
    Respond to incoming text messages from Twilio.
    """
    app.logger.debug("Message from Twilio: %s", repr(dict(request.form)))
    phone_num = request.form['From']
    message = request.form['Body']
    app.logger.debug('Phone number = %s\nMessage = %s',
            phone_num, message)

    # Call the main text message handler
    message = handle_player_text(phone_num, message)
    # Persist changes to the database
    db.session.commit()

    resp = twilio.twiml.Response()

    # Don't send a SMS message back if None was returned
    if message is not None:
        resp.sms(message)

    return str(resp)



def handle_player_text(phone, message, details={}):
    """
    Handles an incoming text from a player.
    """
    message = message.lower()
    app.logger.debug('Processing a message from %s: "%s"', phone, message)

    # TODO: validate phone number and message length

    player, created = Player.get_or_create(phone)
    if created:
        app.logger.debug('Created an account for player %s', phone)

    if player.game_id is not None:
        # Player is already in a game
        game = player.game

        app.logger.debug('Player %s is already known, game is %s', player.phone, player.game.title)
        return player_guess(game, player, message)
    else:
        # Find a game for this player treating the message as the game id
        game_id = message.strip()
        game = Game.query.filter_by(id=message).first()
        if not game:
            return render_template('no_game.txt', game_id=game_id)

        player.game_id = game.id

        # TODO: notify other players that player has joined

        # Respond with a welcome message
        app.logger.debug('Sending join_game response template back to player')
        return player_joined(game, player)


def player_joined(game, player):
    """
    Called when a player successfully joins a game.
    """
    app.logger.debug('Player joined a game')
    current_round = game.rounds[game.current_round]
    hint = current_round.hints[current_round.current_hint]

    # Send confirmation to player along with the current round hint
    return render_template('join_game.txt', game=player.game, player=player, hint=hint)


def player_guess(game, current_player, guess):
    """
    Called when a player makes a guess.
    """
    app.logger.debug('Player %s just guessed "%s"', current_player.phone, guess)
    
                
    

    # Set the players guess
    current_player.guess = guess

    # Get the current round
    current_round = game.rounds[game.current_round]

    # Check if all players have guessed
    round_ready = True
    for player in game.players:
        if player.guess is None:
            round_ready = False

    # if player guess = exit, then drop them from the game
    if guess=="exit":
        current_player.game_id = None
        return render_template('exit.txt')

    if round_ready:
        return guesses_complete(game, current_round)

    return render_template('guess.txt', game=player.game, player=current_player)


def guesses_complete(game, current_round):
    """
    Called when all players have made their guesses for a round.
    """
    app.logger.debug('All guesses have been made for game %s, round %s', game.id, current_round.round_number)

    # Collect all the players who guessed the right answer
    winners = []
    for player in game.players:
        if player.guess == current_round.answer:
            player.points += 1
            winners.append(player)
        player.guess = None

    if len(winners) > 0:
        # One or more people won the round
        return round_complete(game, current_round, winners)

    current_round.current_hint = (current_round.current_hint + 1) % len(current_round.hints)

    if current_round.current_hint == 0:
        # No more hints - NO POINTS FOR YOU!
        return round_complete(game, current_round, [])

    current_hint = current_round.hints[current_round.current_hint]
    broadcast_message([player.phone for player in game.players],
        render_template('next_hint.txt', game=game, round=current_round, hint=current_hint))

    # Don't send anything back to this user directly
    return None


def round_complete(game, current_round, winners):
    """
    Called when a round has ended. winners is a list of players who
    guessed correctly.
    """
    app.logger.debug('Game %s, round %s is now over', game.id, current_round.round_number)

    if len(winners) > 0:
        # Display leaderboard
        broadcast_message([player.phone for player in game.players],
            render_template('round_complete_success.txt', game=game, round=current_round, winners=winners))
    else:
        # Chastise the players
        broadcast_message([player.phone for player in game.players],
            render_template('round_complete_fail.txt', game=game, round=current_round))

    # Advance to the next round and reset this one to the first hint
    current_round.current_hint = 0
    game.current_round = (game.current_round + 1) % len(game.rounds)
    current_round = game.rounds[game.current_round]

    if game.current_round == 0:
        # Game over, clear game and send results
        return game_complete(game)

    # Display next hint
    hint = current_round.hints[current_round.current_hint]
    broadcast_message([player.phone for player in game.players],
        render_template('next_hint.txt', game=game, round=current_round, hint=hint))

    # Don't send anything back to this user directly
    return None


def game_complete(game):
    """
    Called when a game has ended.
    """
    app.logger.debug('Game %s is now over', game.id)

    winner = None
    winning_score = -1
    for player in game.players:
        if player.points > winning_score:
            winning_score = player.points
            winner = player

    # Display leaderboard
    broadcast_message([player.phone for player in game.players],
        render_template('game_over.txt', game=game, winner=winner))

    # Kick all players out of this game
    for player in game.players:
        player.game_id = None

        # Reset player's points
        player.points = 0

    # Don't send anything back to this user directly
    return None


def broadcast_message(numbers, message):
    """
    Send a broadcast text message with Twilio.
    """
    app.logger.debug('BROADCAST: "%s" => %s', message, numbers)

    # For web interface users, add to flash messages
    if 'user_type' in session and session['user_type'] == 'web':
        # TODO: check if this message is for current user
        flash(message, 'broadcast')
        return

    app.logger.debug('Sending message to Twilio')
    client = TwilioRestClient(settings.TWILIO_ACCOUNT, settings.TWILIO_TOKEN)
    for number in numbers:
        client.sms.messages.create(to=number,
                from_=settings.TWILIO_NUMBER,
                body=message)

