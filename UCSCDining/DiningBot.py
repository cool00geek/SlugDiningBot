import datetime
import os
import requests
from bs4 import BeautifulSoup
from UCSCDining import UCSCDining

def get_menu(dining, college_name, meal=""):
    text = ""
    try:
        now_date = datetime.datetime.now().date()
        date = str(now_date.month) +"/" + str(now_date.day) + "/" + str(now_date.year)

        if os.path.exists(dining.get_path() + dining.get_filename(college_name, date)):
            input_source = open(dining.get_path() + dining.get_filename(college_name, date), 'r')
        else:
            url = dining.get_url(college_name, date)
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
    
def help(platform="Telegram", prefix=""):
    help_text = "Welcome to the UCSC Dining hall "  + platform + " bot!"
    help_text += "\nSend any college name to see what they are currently serving"
    help_text += "\n\tFor example, \"" + prefix + "c10\" or \"" + prefix + "rcc\""
    help_text += "\n\nYou can also specify the meal to look into"
    help_text += "\n\tFor example, \"" + prefix + "c9 dinner\" or \"cowell breakfast\""
    return help_text
    
def about(platform="Telegram"):
    text = "Thanks for using the UCSC Dining hall " + platform + " bot!"
    text += "\nThis was created by Vinay (https://github.com/cool00geek/)"
    text += "\nFor more information, contact him at vvenkat3@ucsc.edu"
    return text
