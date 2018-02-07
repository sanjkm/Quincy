# update_dinosaur.py
# Makes required database changes and additions to accounts
# for ABBY being purchased by the Dinosaur Group
# 4/19/2017

import mysql.connector
from mysql.connector import MySQLConnection, Error
from mysql_dbconfig import read_db_config
import sys
from datetime import datetime, timedelta


# Creates table back_month_billed with suitable parameters and such

def create_back_month_billed_table(conn, prev_table_name, old_firm,
                                   new_firm):
    cursor = conn.cursor()

    # Creates the new table
    query = "CREATE TABLE back_month_billed LIKE " + prev_table_name 
    args = ()
    cursor.execute (query, args)

    
    # Copies data from old table into the new table
    query = "INSERT INTO back_month_billed SELECT * FROM " + prev_table_name
    args = ()
    cursor.execute (query, args)

    # Delete all data that does not have old_firm in the
    # BillingCode field

    query = "DELETE FROM back_month_billed " \
            "WHERE BillingCode != '" + old_firm + "'"
    args = ()
    cursor.execute (query, args)
    print "Worked"
    
    # Replace from fields Attributable and BillingCode the old_firm
    # with the new_firm
    query = "UPDATE back_month_billed SET Attributable = " \
            "REPLACE(Attributable, '" + old_firm + "', '" \
            + new_firm + "') WHERE " \
            "INSTR(Attributable, '" + old_firm + "') > 0"
    args = ()
    cursor.execute (query, args)

    query = "UPDATE back_month_billed SET BillingCode = " \
            "REPLACE(BillingCode, '" + old_firm + "', '" \
            + new_firm + "') WHERE " \
            "INSTR(BillingCode, '" + old_firm + "') > 0"
    args = ()
    cursor.execute (query, args)

    conn.commit()

# Add DINO to table codemap
def add_newfirm_codemap (conn, new_firm):

    cursor = conn.cursor()
    query = "INSERT INTO codemap(BillingCode,Firm_Code) " \
            "VALUES('" + new_firm + "','" + new_firm + "')"
    args = ()
    cursor.execute(query,args)
    conn.commit()

# In table line_item, replace old_firm with new_firm in Attributable
# and BillingCode fields
def replace_firm (conn, old_firm, new_firm):
    
    cursor = conn.cursor()
    
    query = "UPDATE line_item SET BillingCode = " \
            "REPLACE(BillingCode, '" + old_firm + "', '" \
            + new_firm + "') WHERE " \
            "INSTR(BillingCode, '" + old_firm + "') > 0"
    args = ()
    cursor.execute (query, args)


    query = "UPDATE line_item SET Attributable = " \
            "REPLACE(Attributable, '" + old_firm + "', '" \
            + new_firm + "') WHERE " \
            "INSTR(Attributable, '" + old_firm + "') > 0"
    args = ()
    cursor.execute (query, args)
    conn.commit()

# Opens the appropriate database and runs all table creation and editing
# functions
def open_database(prev_table_name, old_firm, new_firm):

    db_config = read_db_config ()
    if len(db_config) == 0:
        sys.exit()
    try:
        conn = MySQLConnection (**db_config)
        if conn.is_connected():
            print "Connected to MySQL database"

        # Pass conn into function for each change item
        create_back_month_billed_table(conn, prev_table_name, old_firm,
                                       new_firm)        
        add_newfirm_codemap (conn, new_firm)

        replace_firm (conn, old_firm, new_firm)        

    except Error as e:
        print(e)
        
    finally:
        print "Closing connection"
        conn.close()

def main():
    prev_table_name = 'next_day_invoice'
    old_firm = 'ABBY'
    new_firm = 'DINO'

    open_database(prev_table_name, old_firm, new_firm)

main()
