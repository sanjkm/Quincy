# send_reminder_emails.py
# Determine which email to send to LB, if any
# Generate the email, and then send it out

import os
import datetime
from gen_reminder_emails import genReminderEmail


# Determine if first (1), second(2), or neither email (0) should be sent
def calcWhichReminder():
    now = datetime.datetime.now()

    dow = now.weekday() # 0 for Monday, 6 for Sunday
    
    if dow > 4:
        return 0    
    if now.month == 9 and now.year < 2020: # Labor Day
        return 0
    if now.month == 1:
        return 0

    if now.month == 7 and now.day == 4: # 4th of July
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
                         FIRST_OUTPUT_FILE + SUFFIX,
                         LINES_UNTIL_MONTH, calcRelevantMonth())
        os.system(CURR_DIR + FIRST_REMINDER_CMD_LINE)
        
    elif reminder_num == 2:
        genReminderEmail(CURR_DIR + SECOND_REMINDER_TEMPLATE + \
                         str(genTemplateNumber()) + SUFFIX,
                         SECOND_OUTPUT_FILE + SUFFIX,
                         LINES_UNTIL_MONTH, calcRelevantMonth())
        os.system(CURR_DIR + SECOND_REMINDER_CMD_LINE)

    elif reminder_num == 3:
        genReminderEmail(CURR_DIR + THIRD_REMINDER_TEMPLATE + \
                         str(genTemplateNumber()) + SUFFIX,
                         THIRD_OUTPUT_FILE + SUFFIX,
                         LINES_UNTIL_MONTH, calcRelevantMonth())
        os.system(CURR_DIR + THIRD_REMINDER_CMD_LINE)
        
main()
