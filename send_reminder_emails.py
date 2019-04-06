# send_reminder_emails.py
# Determine which email to send to LB, if any
# Generate the email, and then send it out

import os
import datetime
from gen_reminder_emails import genReminderEmail

# Checks for Labor Day, New Year's eve, or 4th of July issues.
# Returns specific results for these cases
# Returns a pair of numbers: test value (is it a holiday case, 0 or 1)
# and the value to return if it is, zero if it is now
def holiday_check (now):
    if now.month != 9 and now.month != 1 and now.month != 7 and now.month != 4:
        return 0,0

    if now.month == 9:
        if now.year == 2018:
            if now.day == 5:
                return 1,2
            if now.day == 6:
                return 1,3
            return 1,0
            
        if now.year == 2019:
            if now.day == 4:
                return 1,2
            if now.day == 5:
                return 1,3
            return 1,0

    if now.month == 1:
        if now.year == 2019:
            if now.day == 3:
                return 1,2
            if now.day == 4:
                return 1,3
            return 1,0
            
        if now.year == 2020:
            if now.day == 3:
                return 1,2
            if now.day == 6:
                return 1,3
            return 1,0
            
        if now.year == 2021:
            if now.day == 5:
                return 1,2
            if now.day == 6:
                return 1,3
            return 1,0

    if now.month == 7:
        if now.year == 2020:
            if now.day == 2:
                return 1,2
            if now.day == 6:
                return 1,3
            return 1,0

    if now.month == 4:
        if now.year == 2021:
            if now.day == 5:
                return 1,2
            if now.day == 6:
                return 1,3
            return 1,0
    
    return 0,0
            

# Determine if first (1), second(2), third(3),
# or no email (0) should be sent
def calcWhichReminder():
    now = datetime.datetime.now()

    dow = now.weekday() # 0 for Monday, 6 for Sunday

    # pair of values returned - first indicates whether a holiday case,
    # second indicates what should be returned in that case
    holiday_test, holiday_val = holiday_check (now)
    
    if holiday_test == 1:

        return holiday_val
        
    if dow > 4:
        return 0    


    # First weekday of month (note: I don't send these emails anymore
    # so we return zero instead of one)
    if now.day == 1 and dow < 5:
        return 0
    if dow == 0 and (now.day == 2 or now.day == 3):
        return 0

    # Second weekday of month
    if dow == 0 and now.day == 4:
        return 2
    if now.day == 2 and dow < 5:
        return 2
    if now.day == 3 and dow == 1:
        return 2
    if now.day == 4 and dow == 1:
        return 2

    # Third weekday of month
    if now.day == 3:
        return 3
    if now.day == 5 and dow == 0:
        return 3
    if now.day == 5 and dow == 1:
        return 3
    if now.day == 4 and dow == 2:
        return 3
    if now.day == 5 and dow == 2:
        return 3
    if now.day == 5 and now.month == 7 and now.year == 2018:
        return 3
    return 0

# Gets the current month, subtracts 1, and outputs that month name
def calcRelevantMonth():
    now = datetime.datetime.now()
    month_num = now.month
    if month_num == 1:
        month_num = 12
    else:
        month_num = month_num - 1
    month_name = datetime.date(1900, month_num, 1).strftime("%B")
    return month_name

# If multiple templates, can use to return a random number
def genTemplateNumber():
    return 1

def main():

    FIRST_REMINDER_TEMPLATE = 'first_reminder_template'
    SECOND_REMINDER_TEMPLATE = 'second_reminder_template'
    THIRD_REMINDER_TEMPLATE = 'third_reminder_template'
    SUFFIX = '.txt'

    CURR_DIR = '/home/smenon/Quincy/'
    
    FIRST_OUTPUT_FILE = 'first_reminder_email'
    SECOND_OUTPUT_FILE = 'second_reminder_email'
    THIRD_OUTPUT_FILE = 'third_reminder_email'

    LINES_UNTIL_MONTH = 6

    FIRST_REMINDER_CMD_LINE = './first_reminder.sh'
    SECOND_REMINDER_CMD_LINE = './second_reminder.sh'
    THIRD_REMINDER_CMD_LINE = './third_reminder.sh'
    
    reminder_num = calcWhichReminder()
    
    if reminder_num == 1:
        genReminderEmail(CURR_DIR + FIRST_REMINDER_TEMPLATE + \
                         str(genTemplateNumber()) + SUFFIX,
                         CURR_DIR + FIRST_OUTPUT_FILE + SUFFIX,
                         LINES_UNTIL_MONTH, calcRelevantMonth())
        os.system(CURR_DIR + FIRST_REMINDER_CMD_LINE)
        
    elif reminder_num == 2:

        genReminderEmail(CURR_DIR + SECOND_REMINDER_TEMPLATE + \
                         str(genTemplateNumber()) + SUFFIX,
                         CURR_DIR + SECOND_OUTPUT_FILE + SUFFIX,
                         LINES_UNTIL_MONTH, calcRelevantMonth())

        os.system(CURR_DIR + SECOND_REMINDER_CMD_LINE)

    elif reminder_num == 3:
        genReminderEmail(CURR_DIR + THIRD_REMINDER_TEMPLATE + \
                         str(genTemplateNumber()) + SUFFIX,
                         CURR_DIR + THIRD_OUTPUT_FILE + SUFFIX,
                         LINES_UNTIL_MONTH, calcRelevantMonth())
        os.system(CURR_DIR + THIRD_REMINDER_CMD_LINE)
        
main()
