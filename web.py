from flask import Flask, request
from twilio.rest import Client
from web_funcs import update_title, send_message


app = Flask(__name__)

with open('web_cred.txt', 'r') as f:
    accountSID = f.readline().rstrip()
    authToken = f.readline().rstrip()

client = Client(accountSID, authToken)


myTwilioNumber = '+17158008105'


@app.route('/sms', methods=['GET', 'POST'])
def bot():
    incoming_msg = request.values.get('Body', '')
    from_number = request.values.get('From', '')

    if 'title' in incoming_msg.lower():
        try:
            title = incoming_msg.split('title ', 1)[1]
        except:
            title = incoming_msg.split('Title ', 1)[1]
        update_title(title, from_number)
    if 'send' in incoming_msg.lower():
        send_message(incoming_msg, from_number)


app.run()
