# edit_line_item_DB.py
# Makes changes to the appropriate table within the database quincy
# Changes to be made are listed in the listed csv file

import mysql.connector
from mysql.connector import MySQLConnection, Error
from mysql_dbconfig import read_db_config
import sys
from datetime import datetime, timedelta


def edit_database (conn, change_item, table_name, field_list):
    
    cursor = conn.cursor()

    action = change_item[-1]

    if action == 'DEL':
    
        query = "DELETE FROM " + table_name +  \
                " WHERE " + field_list[0] + " LIKE '%" + \
                change_item[0] + "%'" 
        
        for i in range(1, len(change_item) - 2):
            query += (" AND " + field_list[i] + "='" + change_item[i] + "'")

    print query
    args = ()
    cursor.execute (query, args)
    conn.commit()


def open_database(change_list, table_name, field_list):

    db_config = read_db_config ()
    if len(db_config) == 0:
        sys.exit()
    try:
        conn = MySQLConnection (**db_config)
        if conn.is_connected():
            print "Connected to MySQL database"

        # Pass conn into function for each change item
        for change_item in change_list:
            try:
                edit_database (conn, change_item, table_name, field_list)
            except:
                pass
            

    except Error as e:
        print(e)
        
    finally:
        print "Closing connection"
        conn.close()

# Takes the test_index element of the list and moves it to the
# beginning of the list
def place_index_at_beg (test_list, test_index):
    if test_index == 0:
        return test_list
    
    new_list = test_list[:]
    first_item = test_list[test_index]
    del new_list[test_index]
    new_list = [first_item] + new_list
    return new_list
        
# Goes through inputted csv file and gathers all the changes to be made to the
# database
# Valid change checks the date in the first column. If that date is today,then
# change is added
# Each change is a list in the returned list of lists
def determine_db_changes (filename, sep):
    change_list = []
    
    with open(filename, 'r') as f:
        x_beg = f.readline() # firstline is header
        header_data = (x_beg.rstrip()).split(sep)
        field_list = header_data[1:]

        if 'Description' in field_list:
            des_index = field_list.index('Description')
            field_list = place_index_at_beg (field_list, des_index)
        else:
            des_index = 0
        
        for line in f:
            x1 = line.rstrip()
            x_data = x1.split(sep)
            date_str = x_data[0]
            date_val = (datetime.strptime (date_str, '%m/%d/%Y')).date()

            if (datetime.today()).date() == date_val:
                change_list.append(place_index_at_beg(x_data[1:], des_index))
    
    return field_list, change_list
        

def main():

    # Makes changes in the line_item table in the database
    changes_file = 'changes_line_item_DB.csv'
    separator = ','

    field_list, change_list = determine_db_changes (changes_file, separator)

    table_mod = 'line_item'

    # If any changes to make, run the appropriate function
    if len(change_list) > 0:
        open_database(change_list, table_mod, field_list)

    # Makes changes in the invoices table in the database
    changes_file = 'changes_invoices_DB.csv'
    separator = ','

    field_list, change_list = determine_db_changes (changes_file, separator)

    table_mod = 'invoices'
    
    # If any changes to make, run the appropriate function
    if len(change_list) > 0:
        open_database(change_list, table_mod, field_list)
    
main()
    
