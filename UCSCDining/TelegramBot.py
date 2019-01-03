from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import os
from UCSCDining import UCSCDining
import DiningBot



def start(bot, update):
    help_text = DiningBot.help()
    bot.send_message(chat_id=update.message.chat_id, text=help_text)
    
def about(bot, update):
    text = DiningBot.about()
    bot.send_message(chat_id=update.message.chat_id, text=text)
    
def parse(bot, update):
    msg = update.message.text
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
        print(msg)
        bot.send_message(chat_id=update.message.chat_id, text="Sorry, I don't know what college that is!")
    
def unknown(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.")


updater = Updater(token=os.environ.get('TELEGRAM_UCSC_KEY'))
dispatcher = updater.dispatcher

start_handler = CommandHandler('start', start)
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
