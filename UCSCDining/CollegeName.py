import datetime

cowell_names = ['cowell', 'cowell college', 'stevenson', 'stevenson college', 'cowell stevenson']
crown_names = ['crown', 'crown college', 'merrill', 'merrill college', 'crown merrill']
porter_names = ['porter', 'porter college', 'kresge', 'kresge college', 'porter kresge']
rcc_names = ['rcc', 'rachel carson', 'rachel carson college', 'oakes', 'oakes college', 'rachel']
c9_names = ["c9", '9', 'c10', '10', 'college 9', 'college 10', 'college9', 'college10']

def verify_name(college):
    if college.lower() in cowell_names:
        return True
    elif college.lower() in crown_names:
        return True
    elif college.lower() in porter_names:
        return True
    elif college.lower() in rcc_names:
        return True
    elif college.lower() in c9_names:
        return True
    return False

def get_dining_hall(college):
    if college.lower() in cowell_names:
        return "Cowell+Stevenson"
    elif college.lower() in crown_names:
        return "Crown+Merrill"
    elif college.lower() in porter_names:
        return "Porter+Kresge"
    elif college.lower() in rcc_names:
        return "Rachel+Carson+Oakes"
    elif college.lower() in c9_names:
        return "+Colleges+Nine+%26+Ten+"
    return False

def get_college_name(college):
    if college.lower() in cowell_names:
        return "cowell"
    elif college.lower() in crown_names:
        return "crown"
    elif college.lower() in porter_names:
        return "porter"
    elif college.lower() in rcc_names:
        return "rcc"
    elif college.lower() in c9_names:
        return "c9"
    return False

def get_dining_num(college):
    if college.lower() in cowell_names:
        return "05"
    elif college.lower() in crown_names:
        return "20"
    elif college.lower() in porter_names:
        return "25"
    elif college.lower() in rcc_names:
        return "30"
    elif college.lower() in c9_names:
        return "40"
    return False

def get_desired_meal(meal):
    if meal.lower() == "breakfast":
        return 0
    elif meal.lower() == "lunch" or meal.lower() == "brunch":
        return 1
    elif meal.lower() == "dinner":
        return 2
    elif meal.lower() == "night" or meal.lower() == "late night" or meal.lower() == 'late':
        return 3
    else:
        return -1

def get_current_meal():
    now = datetime.datetime.now()
    minu = now.minute
    hour = now.hour
    day = now.weekday()
    if  0 <= day <= 4 :
        if 20 <= hour < 23:
            return 3
        if 14 <= hour < 20:
            return 2
        if 12 <= hour < 2:
            return 1
        if 11 == hour and minu >= 30:
            return 1
        return 0
    else:
        if 20 <= hour < 23:
            return 3
        if 14 <= hour < 20:
            return 2
        if 10 <= hour < 14:
            return 1
        return 0
