from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from bs4 import BeautifulSoup
import datetime
import logging
import os
from UCSCDining import UCSCDining

def get_menu(dining, college_name, meal=""):
    text = ""
    try:
        now_date = datetime.datetime.now().date()
        date = str(now_date.month) +"/" + str(now_date.day) + "/" + str(now_date.year)

        if os.path.exists(dining.get_path() + dining.get_filename(college_name, date)):
            input_source = open(dining.get_path() + dining.get_filename(college_name, date), 'r')
        else:
            url = dining.get_url(college, date)
            input_source = requests.get(url).text
            dining.cache(dining.get_filename(college_name, date), input_source)
            
        soup = BeautifulSoup(input_source, 'lxml')
        startIndex = 2
        text = college_name
        
        if meal:
            meal_id = dining.get_desired_meal(meal)
            if meal_id == -1:
                meal_id = dining.get_current_meal()
        else:
            meal_id = dining.get_current_meal()
            

        for x in range (0,4):
            try:
                # Get the parsed menu based on the starting index
                meal_name, menu = dining.parse_menu(soup, startIndex)
                
                # Print a seperator before the menu if it isn't our first time

                if x == meal_id:
                    if len(menu) == 0:
                        text +="\nNot serving anything!"
                    else:
                        if meal_name == "Late":
                            meal_name = "Late night"
                        text += "\n"+meal_name + " has " + str(len(menu)) + " dishes"
                        for x in menu:
                            text += "\n" + x
                    break
                # The next index has to add 3 and the length of the menu
                startIndex += len(menu) + 3
            except Exception as e:
                # No more meals
                print(e)
                text +="\nNot serving anything!"
                break

        return text

    except Exception as e:
        print("Invalid URL or college")
        print(e)
        return "Sorry, I'm having some trouble processing that"

def start(bot, update):
    help_text = "Welcome to the UCSC Dining hall Telegram bot!"
    help_text += "\nSend any college name to see what they are currently serving"
    help_text += "\n\tFor example, \"c10\" or \"rcc\""
    help_text += "\n\nYou can also specify the meal to look into"
    help_text += '\n\tFor example, \"c9 dinner\" or \"cowell breakfast\"'
    bot.send_message(chat_id=update.message.chat_id, text=help_text)
    
def about(bot, update):
    text = "Thanks for using the UCSC Dining hall Telegram bot!"
    text += "\nThis was created by Vinay (https://github.com/cool00geek/)"
    text += "\nFor more information, contact him at vvenkat3@ucsc.edu"
    bot.send_message(chat_id=update.message.chat_id, text=text)
    
def parse(bot, update):
    msg = update.message.text
    msg_list = msg.split(" ")
    dining = UCSCDining()
    if dining.verify_name(msg_list[0]):
        college_name = dining.get_college_name(msg_list[0])
        meal_name = msg_list[len(msg_list)-1]
        text = get_menu(dining, college_name, meal=meal_name)
        bot.send_message(chat_id=update.message.chat_id, text=text)
    else:
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

parse_handler = MessageHandler(Filters.text, parse)
dispatcher.add_handler(parse_handler)

unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)


updater.start_polling()
updater.idle()
