# update_pleasant_lake.py
# Makes required database changes and additions to accounts
# for change in description of Jones Pleasant Lake platform
# 5/4/2017

import mysql.connector
from mysql.connector import MySQLConnection, Error
from mysql_dbconfig import read_db_config
import sys
from datetime import datetime, timedelta


# In table line_item, replace old_firm with new_firm in Attributable
# and BillingCode fields
def replace_description (conn, old_des, new_des, billing_date):
    
    cursor = conn.cursor()

    # This replaces the old description with the new one in the line_item table
    query = "UPDATE line_item SET Description='" \
            + new_des + "' WHERE Description LIKE " \
            "'%" + old_des + "%'"

    args = ()
    cursor.execute (query, args)

    # This replaces the old description with the new description in the
    # invoices table for the correct billing date

    query = "UPDATE invoices SET Description='" \
            + new_des + "' WHERE Description LIKE " \
            "'%" + old_des + "%' AND Billed_Month='" + billing_date + "'"

    args = ()
    cursor.execute (query, args)
    


    # This will set the new description line's status to Paid instead
    # of Unpaid as it is currently set
    
    query = "UPDATE invoices SET Status='Paid'" \
            " WHERE Description='" + new_des + \
            "' AND Billed_Month='" + billing_date + "'"

    args = ()
    cursor.execute (query, args)

    conn.commit()
    
# Opens the appropriate database and runs all table creation and editing
# functions
def open_database(old_des, new_des, billing_date):

    db_config = read_db_config ()
    if len(db_config) == 0:
        sys.exit()
    try:
        conn = MySQLConnection (**db_config)
        if conn.is_connected():
            print "Connected to MySQL database"

        # Pass conn into function for each change item

        replace_description (conn, old_des, new_des, billing_date)        

    except Error as e:
        print(e)
        
    finally:
        print "Closing connection"
        conn.close()

def get_new_desc (filename, billing_col, desc_col, delim):
    with open(filename, 'r') as f:
        for line in f:
            x1 = line.rstrip()
            x_fields = x1.split (delim)
            billing_date = x_fields[billing_col - 1]
            new_desc = x_fields[desc_col - 1]
            break
    return billing_date, new_desc
def main():

    old_des = 'Pleasant'

    filename, billing_col, desc_col, delim = 'new_pleasant_desc.txt', 1, 3, ','

    billing_date, new_des = get_new_desc (filename, billing_col, desc_col,
                                          delim)
    
    open_database(old_des, new_des, billing_date)

main()
