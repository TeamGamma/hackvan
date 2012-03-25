from flask import render_template, request
from web import app
import settings
from web.database import db
from web.models import (
    Player, Game
)

import twilio.twiml
from twilio.rest import TwilioRestClient
account = "AC97ac1adb110109f39f1f68f8019155c2"
token = "0961b98002d01f307b7893ac695feadd"

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html', settings=settings)

@app.route('/textmessage', methods=['GET', 'POST'])
def text_message():
    """
    Web interface for faking text messages.
    """
    app.logger.debug(repr(dict(request.form)))

    if request.method == 'POST':
        # Form submission
        phone = request.form['phone']
        message = request.form['message']
        response = handle_player_text(phone, message)
        if response:
            return response
        else:
            return 'success'
    else:
        # Show text message form
        return render_template('text_message.html', settings=settings)


def handle_player_text(phone, message, details={}):
    """
    Handles a text from a player.
    """
    message = message.lower()
    app.logger.debug('Processing a message from %s: "%s"', phone, message)

    # TODO: validate phone number and message length

    # Find the player using the phone number, or create a new one
    player = Player.query.filter_by(phone=phone).first()
    if not player:
        app.logger.debug('Player %s does not exist, creating an account', phone)
        player = Player(phone=phone)

        db.session.add(player)
        db.session.commit()

        # Find a game for this player treating the message as the game id
        game_id = message.strip()
        game = Game.query.filter_by(id=message).first()
        if not game:
            return render_template('no_game.txt', game_id=game_id)

        player.game_id = game.id

        db.session.add(player)
        db.session.commit()

        # TODO: notify other players that player has joined

        # Respond with a welcome message
        app.logger.debug('Sending join_game response template back to player')
        return player_joined(game, player)
    else:
        # Player exists, but might not have a game
        if player.game_id is None:
            # Find a game for this player treating the message as the game id
            game_id = message.strip()
            game = Game.query.filter_by(id=message).first()
            if not game:
                return render_template('no_game.txt', game_id=game_id)
            player.game_id = game.id
            db.session.add(player)
            db.session.commit()
        else:
            game = player.game

        app.logger.debug('Player %s is already known, game is %s', player.phone, player.game.id)
        return player_guess(game, player, message)


def player_joined(game, player):
    """ Called when a player successfully joins a game """
    app.logger.debug('Player joined a game')
    current_round = game.rounds[game.current_round]
    hint = current_round.hints[current_round.current_hint]

    # Send confirmation to player along with the current round hint
    return render_template('join_game.txt', game=player.game, player=player, hint=hint)


def player_guess(game, current_player, guess):
    """ Called when a player makes a guess """
    app.logger.debug('Player %s just guessed "%s"', current_player.phone, guess)

    # Set the players guess
    current_player.guess = guess
    db.session.add(current_player)
    db.session.commit()

    current_round = game.rounds[game.current_round]

    # Check if all players have guessed
    round_ready = True
    for player in game.players:
        if player.guess is None:
            round_ready = False

    if round_ready:
        return guesses_complete(game, current_round)

    return render_template('guess.txt', game=player.game, player=current_player)


def guesses_complete(game, current_round):
    """ Called when all players have made their guesses for a round """
    app.logger.debug('All guesses have been made for game %s, round %s', game.id, current_round.round_number)

    # Collect all the players who guessed the right answer
    winners = []
    for player in game.players:
        if player.guess == current_round.answer:
            player.points += 1
            winners.append(player)
        player.guess = None
        db.session.add(player)
    db.session.commit()

    if len(winners) > 0:
        # One or more people won the round
        return round_complete(game, current_round, winners)

    current_round.current_hint = (current_round.current_hint + 1) % len(current_round.hints)
    db.session.add(current_round)
    db.session.commit()

    if current_round.current_hint == 0:
        # No more hints - NO POINTS FOR YOU!
        return round_complete(game, current_round, [])

    current_hint = current_round.hints[current_round.current_hint]
    broadcast_message([player.phone for player in game.players],
        render_template('next_hint.txt', game=game, round=current_round, hint=current_hint))

    # Don't send anything back to this user directly
    return None


def round_complete(game, current_round, winners):
    """ Called when a round has ended """
    app.logger.debug('Game %s, round %s is now over', game.id, current_round.round_number)

    # Advance to the next round and reset this one to the first hint
    current_round.current_hint = 0
    game.current_round = (game.current_round + 1) % len(game.rounds)
    current_round = game.rounds[game.current_round]

    db.session.add(game)
    db.session.add(current_round)
    db.session.commit()

    if len(winners) > 0:
        # Display leaderboard
        broadcast_message([player.phone for player in game.players],
            render_template('round_complete_success.txt', game=game, round=current_round, winners=winners))
    else:
        # Chastise the players
        broadcast_message([player.phone for player in game.players],
            render_template('round_complete_fail.txt', game=game, round=current_round))

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
    """ Called when a game has ended """
    app.logger.debug('Game %s is now over', game.id)

    winner = None
    winning_score = -1
    for player in game.players:
        if player.points > winning_score:
            winner = player

    # Display leaderboard
    broadcast_message([player.phone for player in game.players],
        render_template('game_over.txt', game=game, winner=winner))

    for player in game.players:
        player.game_id = None
        db.session.add(player)

    db.session.commit()
    # Don't send anything back to this user directly
    return None


@app.route("/sms", methods=['POST'])
def process_message():
    """Respond to incoming text messages """
    app.logger.debug(repr(dict(request.form)))
    phone_num = request.form['From']
    message = request.form['Body']
    app.logger.debug('Phone number = %s\nMessage = %s',
            phone_num, message)

    message = handle_player_text(phone_num, message)

    resp = twilio.twiml.Response()

    # Don't send a SMS message back if None was returned
    if message is not None:
        resp.sms(message)

    return str(resp)


def broadcast_message(numbers, message):
    """ Send a broadcast text message """
    app.logger.debug('BROADCAST: "%s" => %s', message, numbers)

    client = TwilioRestClient(account, token)
    for number in numbers:
        client.sms.messages.create(to=number,
                from_="+17788002763",
                body=message)

