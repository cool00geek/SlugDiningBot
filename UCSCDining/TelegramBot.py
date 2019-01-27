#!/usr/bin/env python3

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import os
from UCSCDining import UCSCDining
import DiningBot

def print_msg(update):
    print(update.message.from_user.username + " sent message: " + update.message.text)

def start(bot, update):
    print_msg(update)
    DiningBot.store_from(str(update.message.from_user.username), "telegram_users.txt")
    help_text = DiningBot.help(prefix="/")
    bot.send_message(chat_id=update.message.chat_id, text=help_text)
    
def about(bot, update):
    print_msg(update)
    DiningBot.store_from(str(update.message.from_user.username), "telegram_users.txt")
    text = DiningBot.about()
    bot.send_message(chat_id=update.message.chat_id, text=text)
    
def parse(bot, update):
    print_msg(update)
    DiningBot.store_from(str(update.message.from_user.username), "telegram_users.txt")
    msg = update.message.text
    if msg.lower() == "hello there":
        bot.send_message(chat_id=update.message.chat_id, text="General Kenobi")
        return
    msg_list = msg.split(" ")
    if msg_list[0].lower() == "/menu" or msg_list[0].lower() == "menu":
        del msg_list[0]
    dining = UCSCDining()
    if dining.verify_name(msg_list[0]):
        college_name = dining.get_college_name(msg_list[0])
        meal_name = msg_list[len(msg_list)-1]
        text = DiningBot.get_menu(dining, college_name, meal=meal_name)
        bot.send_message(chat_id=update.message.chat_id, text=text)
    else:
        print("TG-err: " + msg)
        bot.send_message(chat_id=update.message.chat_id, text="Sorry, I don't know what college that is!")

def search(bot, update):
    print_msg(update)
    DiningBot.store_from(str(update.message.from_user.username), "telegram_users.txt")

    msg = update.message.text
    msg_list = msg.split(" ")
    del msg_list[0]
    dining = UCSCDining()
    meal = ""
    meal_id = dining.get_desired_meal(msg_list[len(msg_list) - 1])
    print(meal_id)
    if not meal_id == -1:
        meal = msg_list[len(msg_list) - 1]
        del msg_list[len(msg_list) - 1]
    msg_str = ""
    for x in msg_list:
        msg_str += x + " "
    msg_str = msg_str[:-1]
    bot.send_message(chat_id=update.message.chat_id, text=DiningBot.search(msg_str, meal=meal))
    

def unknown(bot, update):
    print_msg(update)
    DiningBot.store_from(str(update.message.from_user.username), "telegram_users.txt")
    bot.send_message(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.")


updater = Updater(token=os.environ.get('TELEGRAM_UCSC_KEY'))
dispatcher = updater.dispatcher

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

start_handler = CommandHandler('search', search)
dispatcher.add_handler(start_handler)

help_handler = CommandHandler('help', start)
dispatcher.add_handler(help_handler)

about_handler = CommandHandler('about', about)
dispatcher.add_handler(about_handler)

menu_handler = CommandHandler('menu', parse)
dispatcher.add_handler(menu_handler)

parse_handler = MessageHandler(Filters.text, parse)
dispatcher.add_handler(parse_handler)

unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)


updater.start_polling()
updater.idle()
