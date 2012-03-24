from flask import render_template, request
from web import app
import settings
from web.database import db
from web.models import (
    Player, Game, Round, Hint,
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
        return handle_player_text(phone, message)
    else:
        # Show text message form
        return render_template('text_message.html', settings=settings)


def handle_player_text(phone, message, details={}):
    """
    Handles a text from a player.
    """
    app.logger.debug('Processing a message from %s: "%s"', phone, message)
    # TODO: validate phone number and message length

    # Find the player using the phone number, or create a new one
    player = Player.query.filter_by(phone=phone).first()
    if not player:
        app.logger.debug('Player %s does not exist, creating an account', phone)
        player = Player(phone=phone)

        # Find a game for this player based on the message and optional details
        player.game = find_game(message.strip(), details)

        db.session.add(player)
        db.session.commit()

        # TODO: notify other players that player has joined

        # Respond with a welcome message
        app.logger.debug('Sending join_game response template back to player')
        return render_template('join_game.txt', game=player.game, player=player)
    else:
        app.logger.debug('Player %s is already known, game is %s', player.phone, player.game.id)
        return 'You just guessed "%s". Rest of game is not implemented yet' % message
    



def find_game(message, details={}):
    # TODO: look up game from database
    return Game.query.first()


@app.route("/sms", methods=['POST'])
def process_message():
    """Respond to incoming text messages """
    app.logger.debug(repr(dict(request.form)))
    phone_num = request.form['From']
    message = request.form['Body']
    app.logger.debug('Phone number = %s\nMessage = %s',
            phone_num, message)
    message = handle_player_text(phone_num, message)
    app.logger.debug("Sending %s to User", message)
    resp = twilio.twiml.Response()
    resp.sms(message)
    #app.logger.debug(str(resp))
    return str(resp)


def reply_message(numbers, message):
    """ Send a broadcast text message """
    client = TwilioRestClient(account, token)
    for number in numbers:
        client.sms.messages.create(to=number,
                from_="+17788002763",
                body=message)

