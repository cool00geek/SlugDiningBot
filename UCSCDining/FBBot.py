#!/usr/bin/env python3

from pymessenger.bot import Bot
from flask import Flask, request
from waitress import serve
import os
from UCSCDining import UCSCDining
import DiningBot

app = Flask(__name__)
ACCESS_TOKEN = os.environ.get('FB_ACCESS_TOKEN')
VERIFY_TOKEN = os.environ.get('FB_VERIFY_TOKEN')
bot = Bot(ACCESS_TOKEN)

def parse(msg):
    msg_list = msg.split(" ")
    if msg_list[0].lower() == "/menu":
        del msg_list[0]
    dining = UCSCDining()
    if dining.verify_name(msg_list[0]):
        college_name = dining.get_college_name(msg_list[0])
        meal_name = msg_list[len(msg_list)-1]
        text = DiningBot.get_menu(dining, college_name, meal=meal_name)
        bot.send_message(chat_id=update.message.chat_id, text=text)
    else:
        print("FB-err: " + msg)
        bot.send_message(chat_id=update.message.chat_id, text="Sorry, I don't know what college that is!")

#We will receive messages that Facebook sends our bot at this endpoint 
@app.route("/", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook.""" 
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    #if the request was not get, it must be POST and we can just proceed with sending a message back to user
    else:
        # get whatever message a user sent the bot
       output = request.get_json()
       for event in output['entry']:
          messaging = event['messaging']
          for message in messaging:
            if message.get('message'):
                #Facebook Messenger ID for user so we know where to send response back to
                recipient_id = message['sender']['id']
                if message['message'].get('text'):
                    incoming = message['message'].get('text')
                    if incoming.startswith('/start') or incoming.startswith('/help'):
                        msg = DiningBot.help(platform="Messenger", prefix="/")
                    elif incoming.startswith('/about'):
                        msg = DiningBot.about(platform="Messenger")
                    elif incoming.startswith('/menu'):
                        msg = parse(message.content)
                    elif incoming.startswith('/'):
                        msg = "I don't understand that command!"
                    response_sent_text = get_message()
                    send_message(recipient_id, msg)
    return "Message Processed"


def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error 
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'

#uses PyMessenger to send response to user
def send_message(recipient_id, response):
    #sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"

if __name__ == "__main__":
    serve(app, host='127.0.0.1', port=8080)
    #app.run()
