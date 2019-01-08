import plivo
from flask import Flask, request, Response
from waitress import serve
import requests
import DiningBot
import os

app = Flask(__name__)

@app.route("/receive_sms/", methods=['GET','POST'])
def receive_sms():
    # Sender's phone numer
    from_number = request.values.get('From')
    # Receiver's phone number - Plivo number
    to_number = request.values.get('To')
    # The text which was received
    text = request.values.get('Text')

    # Print the message
    print('Message received - From: ' + from_number + ', To: ' + to_number + ', Text: ' + text)

    if text.lower().startswith('start') or text.lower().startswith('help'):
        print("We are starting now")
        msg = DiningBot.help(platform="SMS", prefix="")
    elif text.lower().startswith('about'):
        msg = DiningBot.about(platform="SMS")
    elif text.lower().startswith("hello there"):
        msg = "General Kenobi"
    elif text.lower().startswith("menu"):
        msg = DiningBot.parse(text, platform="SMS", prefix="")
    else:
        msg = DiningBot.parse(text, platform="SMS", prefix="")
        if not msg:
            return "Message received", 200
        else:
            pass

    headers = {
        'Content-Type': 'application/json'
    }

    data = '{"src": "' + to_number + '","dst": "' + from_number + '","text": "'+ msg + '"}'

    auth_id = os.environ.get("PLIVO_AUTH")
    auth_token = os.environ.get("PLIVO_TOKEN")

    url = 'https://api.plivo.com/v1/Account/' + auth_id + '/Message/'
    response = requests.post(url, headers=headers, data=data, auth=(auth_id, auth_token))

    return "Message sent", 200

if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=57920)
    #app.run(host='0.0.0.0', port=57920)
