from flask import Flask, request
import twilio.twiml
from twilio.rest import TwilioRestClient

app = Flask(__name__)

account = "AC97ac1adb110109f39f1f68f8019155c2"
token = "0961b98002d01f307b7893ac695feadd"

@app.route("/", methods=['POST'])
def process_message():
    """Respond to incoming calls with a simple text message."""
    app.logger.debug(repr(dict(request.form)))
    phone_num = request.form['From']
    message = request.form['Body']
    app.logger.debug('Phone number = %s\nMessage = %s',
            phone_num, message)
    # message = -- Call Rob's Function --
    message = "Received"
    resp = twilio.twiml.Response()
    resp.sms(message)
    #app.logger.debug(str(resp))
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)

def reply_message(numbers, message):

    client = TwilioRestClient(account, token)
    for number in numbers:
        client.sms.messages.create(to=number,
                from_="+17788002763",
                body=message)

