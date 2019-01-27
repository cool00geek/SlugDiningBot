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
        
        if not meal=="":
            meal_id = dining.get_desired_meal(meal)
            if meal_id == -1:
                meal_id = dining.get_current_meal()
        else:
            meal_id = dining.get_current_meal()

        for x in range (0,4):
            try:
                # Get the parsed menu based on the starting index
                meal_name, menu = dining.parse_menu(soup, startIndex)
                
                meal_name, menu = dining.parse_menu(soup, startIndex)
                if x==0 and meal_name == "Lunch":
                    meal_id -= 1
                elif x==0 and meal_name == "Dinner":
                    meal_id -= 2
                elif x==0 and meal_name == "Late":
                    meal_id -= 3
                
                # Print a seperator before the menu if it isn't our first time

                if x == meal_id:
                    if len(menu) == 0:
                        text +="\nDining Hall Closed!"
                    else:
                        if meal_name == "Late":
                            meal_name = "Late Night"
                        text += "\n"+meal_name + " has " + str(len(menu)) + " dishes"
                        for x in menu:
                            text += "\n" + x
                    break
                # The next index has to add 3 and the length of the menu
                startIndex += len(menu) + 3
            except Exception as e:
                # No more meals
                print(e)
                text +="\nDining Hall Closed!"
                break

        return text

    except Exception as e:
        print("Invalid URL or college")
        print(e)
        return "Sorry, I'm having some trouble processing that"
    
def help(platform="Telegram", prefix=""):
    help_text = "Welcome to the UCSC Dining hall "  + platform + " bot!"
    help_text += "\nSend any college name, preceded by '" + prefix+"menu' to see what they are currently serving"
    help_text += "\n\tFor example, '" + prefix + "menu c10' or '" + prefix + "menu rcc'"
    help_text += "\n\nYou can also specify the meal to look into"
    help_text += "\n\tFor example, '" + prefix + "menu c9 dinner' or '" + prefix + "menu cowell breakfast'"
    return help_text
    
def about(platform="Telegram"):
    text = "Thanks for using the UCSC Dining hall " + platform + " bot!"
    text += "\nFor some information about the advanced usage, checkout https://cool00geek.github.io/SlugDiningBot/"
    text += "\nThis was created by Vinay (https://github.com/cool00geek/)"
    text += "\nFor more information, contact him at vvenkat3@ucsc.edu"
    text += "\n\nIf you really enjoy using this bot, consider making a donation! https://cool00geek.github.io/SlugDiningBot/about.html"
    return text

def parse(msg, platform="GEN", prefix=""):
    msg_list = msg.split(" ")
    if msg_list[0].lower() == prefix + "menu":
        del msg_list[0]
    dining = UCSCDining()
    if dining.verify_name(msg_list[0]):
        college_name = dining.get_college_name(msg_list[0])
        meal_name = msg_list[len(msg_list)-1]
        text = get_menu(dining, college_name, meal=meal_name)
    else:
        print(platform + "-err: " + msg)
        #text="Sorry, I don't know what college that is!"
        return None
    return text

def search(keyword, meal=""):
    dining = UCSCDining()
    cowell = get_menu(dining,"cowell", meal)
    crown = get_menu(dining, "crown", meal)
    cn = get_menu(dining, "c9", meal)
    porter = get_menu(dining, "porter", meal)
    rcc = get_menu(dining, "rcc", meal)
    #print(porter)


def store_from(text, filename):
    dining = UCSCDining()
    f = open(dining.get_path() + filename, 'a+')
    f.write(text)
    f.write('\n')
    f.close()


if __name__ == '__main__':
    search("Hello")