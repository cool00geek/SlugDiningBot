#!/usr/bin/env python3

from bs4 import BeautifulSoup
import sys
import argparse
import requests
import datetime
import os
from datetime import datetime as dt
from Scraper import parse_menu, print_menu, get_filename, get_path, cache
from URL import get_url
from CollegeName import verify_name, get_current_meal, get_desired_meal

def main(infile="", college="", datestr="", nocache=False):
    using_cache = False
    # If we want a file, open the file
    if infile:
        try:
            input_source = open(infile,'r')
        except:
            print("File not found!")
            exit(130)
    # In order to webscrape we need the college and date
    elif college and datestr:
        try:
            if not verify_name(college):
                print("Invalid college name!")
                exit (134)
            month,day,year = datestr.split('/')
            try :
                datetime.datetime(int(year),int(month),int(day))
            except :
                print("Invalid date format!")
                exit(135)
            date = datestr
            url = get_url(college, datestr)
            if not nocache and os.path.exists(get_path() + get_filename(college, date)):
                input_source = open(get_path() + get_filename(college, date), 'r')
                using_cache=True
            else:
                input_source = requests.get(url).text
        except Exception as e:
            print(e)
            print("Invalid URL, college, or date")
            exit(132)
    elif college:
        try:
            if not verify_name(college):
                print("Invalid college name!")
                exit(134)
            now_date = datetime.datetime.now().date()
            date = str(now_date.month) +"/" + str(now_date.day) + "/" + str(now_date.year)
            url = get_url(college, date)
            if not nocache and os.path.exists(get_path() + get_filename(college, date)):
                input_source = open(get_path() + get_filename(college, date), 'r')
                using_cache=True
            else:
                input_source = requests.get(url).text
        except Exception as e:
            print("Invalid URL or college")
            print(e)
            exit(132)
    else:
        print("Incorrect arguments!")
        exit(131)

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
                cache(get_filename(college, date), input_source)
        

    # Create the soup object, and parse it using lxml
    soup = BeautifulSoup(input_source, 'lxml')

    # Starting index has to be 2 for breakfast
    startIndex = 2

    return soup,startIndex
    
    
if __name__ == '__main__':
    description = 'Program to display UCSC dining hall options in all dining halls'
    parser = argparse.ArgumentParser(description = description)
    parser.add_argument("-f", "--file", help="use an input file")
    parser.add_argument("-c", "--college", help="specify college: \"cowell\", \"stevenson\", \"merrill\", \"crown\", \"kresge\", \"porter\", \"oakes\", \"rcc\", \"c9\", \"c10\"")
    parser.add_argument("-d", "--date", help="Specify the date in MM/DD/YYYY form")
    parser.add_argument('-a', '--all', dest='all_meals', help="Print the entire menu regardless of time and meal", action='store_true')
    parser.add_argument('-m', '--meal', help="Specify the meal you want")
    parser.add_argument('-i', '--invalidate-cache', dest='no_cache', help="Do not use the cache and force a pull from the internet", action='store_true')
    parser.set_defaults(all_meals=False)
    args = parser.parse_args()
    
    soup, startIndex = main(infile=args.file, college=args.college, datestr=args.date, nocache=args.no_cache)
    
    # 4 meals so do it 4 times
    desired_meal = get_current_meal()
    if args.meal:
        meal = get_desired_meal(args.meal)
        if meal == -1:
            print("Invalid meal specified!")
            exit(139)
        else:
            desired_meal = meal


    for x in range (0,4):
        try:
            # Get the parsed menu based on the starting index
            meal, menu = parse_menu(soup, startIndex)
            
            # Print a seperator before the menu if it isn't our first time

            if args.all_meals:
                if x != 0:
                    print()
                # Print the menu
                print_menu(meal,menu)
            elif x == desired_meal:
                print_menu(meal,menu)
            # The next index has to add 3 and the length of the menu
            startIndex += len(menu) + 3
        except:
            # No more meals
            pass
