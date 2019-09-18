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
            
        text = college_name
        
        if not meal=="":
            desired_meal = dining.get_desired_meal(meal)
            if desired_meal == -1:
                desired_meal = dining.get_current_meal()
        else:
            desired_meal = dining.get_current_meal()

        if nocache or not (os.path.exists(dining.get_path() + dining.get_filename(college,date)) and os.path.isfile(dining.get_path() + dining.get_filename(college,date))):
            driver = dining.open_driver()
            cache_text = ""
            for x in range (0,4):
                try:
                    # Get the parsed menu based on the starting index
                    try:
                        meal_name, menu = dining.parse_menu(driver, college, dining.get_url(college,date), x)
                    except Exception as e: print(e)
                    
                    # Start saving the text to cache
                    cache_text += meal_name + '\n'
                    for i in menu:
                        cache_text += i + '\n'
                    cache_text += '\n'
                    
                    if x==0 and meal_name == "Lunch":
                        desired_meal -= 1
                    elif x==0 and meal_name == "Dinner":
                        desired_meal -= 2
                    elif x==0 and meal_name == "Late":
                        desired_meal -= 3
                    
                    # Print a seperator before the menu if it isn't our first time
                    if x == desired_meal:
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
                except:
                    print(e)
                    text +="\nDining Hall Closed!"
                    break
            driver.quit()
            
            # Cache it
            if not infile:
                if using_cache:
                    pass
                else:
                    target_dt = dt.strptime(date, '%m/%d/%Y')
                    target_day = target_dt.day
                    today = target_dt.now().date()
                    today_day = today.day
                    if target_day < today_day or today_day + 7 < target_day:
                        pass # Bad date
                    else:
                        dining.cache(dining.get_filename(college, date), cache_text)
        else: # This is using the cache
            with open(dining.get_path() + dining.get_filename(college,date), 'r') as cache_file:
                meals = list()
                meals.append(list())
                meals.append(list())
                meals.append(list())
                meals.append(list())
                current_list = 0
                for line in cache_file:
                    if "Breakfast" in line:
                        current_list = 0
                        continue
                    elif "Lunch" in line:
                        current_list = 1
                        continue
                    elif "Dinner" in line:
                        current_list = 2
                        continue
                    elif "Late" in line:
                        current_list = 3
                        continue
                    elif line == "":
                        continue
                    else:
                        pass
                    meals[current_list].append(line)
                if desired_meal == 0:
                    if len(menu) == 0:
                        text +="\nDining Hall Closed!"
                    else:
                        text += "\nBreakfast has " + str(len(meals[0])) + " dishes"
                        for x in menu:
                            text += "\n" + x
                    break
                elif desired_meal == 1:
                    if len(menu) == 0:
                        text +="\nDining Hall Closed!"
                    else:
                        text += "\nLunch has " + str(len(meals[0])) + " dishes"
                        for x in menu:
                            text += "\n" + x
                    break
                elif desired_meal == 2:
                    if len(menu) == 0:
                        text +="\nDining Hall Closed!"
                    else:
                        text += "\nDinner has " + str(len(meals[0])) + " dishes"
                        for x in menu:
                            text += "\n" + x
                    break
                else:
                    if len(menu) == 0:
                        text +="\nDining Hall Closed!"
                    else:
                        text += "\nLate Night has " + str(len(meals[0])) + " dishes"
                        for x in menu:
                            text += "\n" + x
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
    help_text += "\n\nFor additional information, check out https://cool00geek.github.io/SlugDiningBot/"
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

def find_items(menu_str, college, keyword):
    to_return = ""
    menu_list = menu_str.split("\n")
    if len(menu_list) == 1:
        return to_return
    menu_list.pop(0)
    menu_list.pop(0)
    for item in menu_list:
        if keyword.lower() in item.lower():
            to_return += "\n" + item
    if not to_return == "":
        to_return = college + to_return
    return to_return



def search(keyword, meal=""):
    dining = UCSCDining()
    cowell = get_menu(dining,"cowell", meal)
    crown = get_menu(dining, "crown", meal)
    cn = get_menu(dining, "c9", meal)
    porter = get_menu(dining, "porter", meal)
    rcc = get_menu(dining, "rcc", meal)

    if "Dining Hall Closed!" in cowell:
        cowell = ""
    if "Dining Hall Closed!" in crown:
        crown = ""
    if "Dining Hall Closed!" in cn:
        cn = ""
    if "Dining Hall Closed!" in porter:
        porter = ""
    if "Dining Hall Closed!" in rcc:
        rcc = ""

    cowell = find_items(cowell, "cowell", keyword)
    crown = find_items(crown, "crown", keyword)
    cn = find_items(cn, "c9", keyword)
    porter = find_items(porter, "porter", keyword)
    rcc = find_items(rcc, "rcc", keyword)

    to_return = ""

    if not cowell == "":
        to_return += cowell
        pass
    if not crown == "":
        if not to_return == "":
            to_return += "\n"
        to_return += crown
        pass
    if not cn == "":
        if not to_return == "":
            to_return += "\n"
        to_return += cn
        pass
    if not porter == "":
        if not to_return == "":
            to_return += "\n"
        to_return += porter
        pass
    if not rcc == "":
        if not to_return == "":
            to_return += "\n"
        to_return += rcc
        pass


    if not to_return == "":
        if not meal == "":
            to_return = meal + "\n" + to_return
    return to_return

def store_from(text, filename):
    dining = UCSCDining()
    f = open(dining.get_path() + filename, 'a+')
    f.write(text)
    f.write('\n')
    f.close()


#if __name__ == '__main__':
#    print(search("jambalaya", "lunch"))
