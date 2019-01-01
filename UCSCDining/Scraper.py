from bs4 import BeautifulSoup
from pathlib import Path
from datetime import datetime
import sys
import os
from CollegeName import get_college_name

# Parse the menu
def parse_menu(soup, start_index):
    # Since the menu is in table form, get the tables
    tables = soup.find_all('table')

    # Create a list for the actual text. There are a LOT of empty lines
    menu = list()
    for i in tables:
        # If there is some text, add it to the menu
        if i.text.strip() != "":
            menu.append(i.text)

    # Get the meal label (breakfast, lunch, etc)
    meal_label = menu[start_index].strip().split(" ")[0].strip()

    # Since there are still a bunch of other text we don't need, create a new list with just the meal items
    meal_items = list()
    # Split it by new line
    for item in menu[start_index+1].split('\n'):
        # And if it isn't empty, it's a dish, so add it
        if item.strip() != '':
            meal_items.append(item.strip())
    
    # Finally return the label and the list with all the items
    return meal_label, meal_items

def print_menu(meal, menu):
    # Convert Late -> Late Night
    if meal == "Late":
        meal = "Late Night"
        
    # Print the heading for the meal (The name and the number of dishes it has
    print(meal + ": " + str(len(menu)))
    # And print every dish in the menu
    for dish in menu:
        print(dish)

def get_path():
    home = str(Path.home())
    cache_dir = home + "/.cache/UCSCDining/"
    if not os.path.isdir(cache_dir):
        os.mkdir(cache_dir)
    return cache_dir

def get_filename(college, date):
    dt = datetime.strptime(date, '%m/%d/%Y')
    date = str(dt.year) + "-" + str(dt.month) + "-" + str(dt.day)
    college_name = get_college_name(college)
    return date + "_" + college_name + ".htm"

def cache(filename, text):
    cache_dir = get_path()
    menu = open(cache_dir + filename, "w")
    menu.write(text)
    menu.close()
    
