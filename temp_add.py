# temp_add.py
# Creates a temporary table with this month's line items,
# and adds those Unpaid line items to the invoices table

import mysql.connector
from mysql.connector import MySQLConnection, Error
from mysql_dbconfig import read_db_config
import sys
from calendar import monthrange
from datetime import datetime, timedelta

# Creates the temporary monthly table, copied directly from
# the generic line_item table
def create_init_table():
    """ Comment testing """

    db_config = read_db_config ()
    if len(db_config) == 0:
        sys.exit()
    try:

        conn = MySQLConnection (**db_config)
        if conn.is_connected():
            print "Connected to MySQL database"

        cursor = conn.cursor()
        
        query = "CREATE TABLE month_temp " \
                "SELECT * FROM line_item"
        args = ()

        cursor.execute (query, args)
        conn.commit()

    except Error as e:
        print(e)
        
    finally:
        print "Closing connection"
        cursor.close()
        conn.close()

# This takes the month_temp table, and adds 4 columns to its beginning,
# 3 of which are date columns
# It also switches the position of the Attributable and BillingCode cols
def modify_table_invoice_form():
    """ Comment testing """

    db_config = read_db_config ()
    if len(db_config) == 0:
        sys.exit()
    try:
        conn = MySQLConnection (**db_config)
        if conn.is_connected():
            print "Connected to MySQL database"

        cursor = conn.cursor()

        query = "ALTER TABLE month_temp " \
                "CHANGE COLUMN Attributable Attributable VARCHAR(25) " \
                "NOT NULL AFTER BillingCode, " \
                "ADD COLUMN INV_CODE VARCHAR(25) NULL FIRST, " \
                "ADD COLUMN Invoice_Date DATE NOT NULL AFTER INV_CODE, " \
                "ADD COLUMN Billed_Month DATE NOT NULL AFTER Invoice_Date, " \
                "ADD COLUMN Service_Month DATE NOT NULL AFTER Billed_Month, " \
                "ADD COLUMN Firm_Code VARCHAR(25) NOT NULL AFTER Payee"
        args = ()
        cursor.execute (query, args)
        conn.commit()

    except Error as e:
        print(e)
        
    finally:
        print "Closing connection"
        cursor.close()
        conn.close()

# This will fill the values of Firm_Code based on the values in
# the table codemap mapping to the field BillingCode (in both tables)
def add_firm_code():
    db_config = read_db_config ()
    if len(db_config) == 0:
        sys.exit()
    try:
        conn = MySQLConnection (**db_config)
        if conn.is_connected():
            print "Connected to MySQL database"

        cursor = conn.cursor()

        query = "UPDATE month_temp AS t1, " \
                "codemap AS t2 " \
                "SET t1.Firm_Code = t2.Firm_Code " \
                "WHERE t1.BillingCode = t2.BillingCode"
        args = ()
        cursor.execute (query, args)
        conn.commit()

    except Error as e:
        print(e)
        
    finally:
        print "Closing connection"
        cursor.close()
        conn.close()

#-----------------------------------------------------------------------------
# This updates the 3 date fields that start the table with the relevant
# dates in MySQL format
# It inputs the same date for all rows. Later functions will address the
# exceptions to this
def update_date_info (month_num):
    dt = calc_full_date (month_num) # datetime object

    date_str = (dt.__str__()).split(' ')[0]
    
    db_config = read_db_config ()
    
    if len(db_config) == 0:
        sys.exit()
    try:
        conn = MySQLConnection (**db_config)
        if conn.is_connected():
            print "Connected to MySQL database"
        cursor = conn.cursor()

        query = "UPDATE month_temp AS t1 " \
                "SET t1.Invoice_Date = %s, " \
                "t1.Billed_Month = %s, " \
                "t1.Service_Month = %s"
        args = (date_str, date_str, date_str)
        cursor.execute (query, args)
        conn.commit()

    except Error as e:
        print(e)
        
    finally:
        print "Closing connection"
        cursor.close()
        conn.close()
    

def calc_full_date (month_num):
    data_month = int(month_num)

    # double check relevant year
    dt = datetime.now()
    tt = dt.timetuple()
    curr_yr, curr_month = tt.tm_year, tt.tm_mon
    if curr_month >= data_month:
        data_yr = curr_yr
    else:
        data_yr = curr_yr - 1
        
    days_in_month = monthrange (data_yr, data_month)[1]

    return datetime(data_yr, data_month, days_in_month)

# Looks at table next_day_invoice to set those invoices to the
# correct InvoiceDate and ServiceMonth
def invoice_date_exceptions (month_num):

    dt = calc_full_date (month_num) # datetime object
    td = timedelta(1) # 1 day

    invoice_dt = dt + td
    invoice_date_str = (invoice_dt.__str__()).split(' ')[0]

    days_in_month = monthrange (invoice_dt.year, invoice_dt.month)[1]
    service_dt = dt + timedelta(days_in_month) #last day of next month
    service_date_str = (service_dt.__str__()).split(' ')[0]
        
    db_config = read_db_config ()
    
    if len(db_config) == 0:
        sys.exit()
    try:
        conn = MySQLConnection (**db_config)
        if conn.is_connected():
            print "Connected to MySQL database"
        cursor = conn.cursor()

        query = "UPDATE month_temp AS t1, next_day_invoice AS t2 " \
                "SET t1.Invoice_Date = %s, " \
                "t1.Service_Month = %s " \
                "WHERE t1.Attributable = t2.Attributable AND " \
                "t1.BillingCode = t2.BillingCode AND " \
                "t1.Description = t2.Description" 

        args = (invoice_date_str, service_date_str)
        cursor.execute (query, args)
        conn.commit()

    except Error as e:
        print(e)
        
    finally:
        print "Closing connection"
        cursor.close()
        conn.close()

# This will update the table for the line items whose service month
# is one month later than the general service month (pay in advance).
# Line items are pulled from the post_month_service table
def service_month_exceptions (month_num):

    dt = calc_full_date (month_num) # datetime object
    td = timedelta(1) # 1 day

    next_day_dt = dt + td # first day of next month

    reg_date_str =  (dt.__str__()).split(' ')[0]

    days_in_month = monthrange (next_day_dt.year, next_day_dt.month)[1]
    service_dt = dt + timedelta(days_in_month) #last day of next month
    service_date_str = (service_dt.__str__()).split(' ')[0]
    
    db_config = read_db_config ()
    if len(db_config) == 0:
        sys.exit()
    try:
        conn = MySQLConnection (**db_config)
        if conn.is_connected():
            print "Connected to MySQL database"
        cursor = conn.cursor()

        query = "UPDATE month_temp AS t1, post_month_service AS t2 " \
                "SET t1.Service_Month = %s, " \
                "t1.Billed_Month = %s " \
                "WHERE t1.Attributable = t2.Attributable " \
                "AND t1.BillingCode = t2.BillingCode " \
                "AND t1.Description = t2.Description" 

        args = (service_date_str, reg_date_str)
        cursor.execute (query, args)
        conn.commit()

    except Error as e:
        print(e)
        
    finally:
        print "Closing connection"
        cursor.close()
        conn.close()

# Makes a table mapping invoice dates to the equivalent Excel integer
# representation of that date
def create_invcode_table(month_num):

    db_config = read_db_config ()
    if len(db_config) == 0:
        sys.exit()
    try:
        conn = MySQLConnection (**db_config)
        if conn.is_connected():
            print "Connected to MySQL database"

        cursor = conn.cursor(buffered=True)
        
        query = """ 
                   CREATE TABLE invoice_codemap (
                   Invoice_Date DATE NOT NULL, 
                   Invoice_Code DECIMAL(6,0) NOT NULL)
                """       
        cursor.execute (query)
            
    except Error as e:
        print(e)
        
    finally:
        print "Closing connection"
        cursor.close()
        conn.close()

def update_invoice_code_table (month_num):

    dt = calc_full_date (month_num) # last day of curr month
    next_day_dt = dt + timedelta(1) # first day of next month

    days_in_month = monthrange (next_day_dt.year, next_day_dt.month)[1]        
    next_month_dt = dt + timedelta(days_in_month)

    curr_month_str = date_obj_str (dt)
    next_day_str = date_obj_str (next_day_dt)
    next_month_str = date_obj_str (next_month_dt)
    
    db_config = read_db_config ()
    if len(db_config) == 0:
        sys.exit()
    try:
        conn = MySQLConnection (**db_config)
        if conn.is_connected():
            print "Connected to MySQL database"

        cursor = conn.cursor()

        query = """
                   INSERT INTO invoice_codemap  
                   VALUES (%s, %s), (%s, %s), (%s, %s)
                """           
        curr_month_val =  calc_Excel_val (dt)
        args = (curr_month_str, curr_month_val,
                next_day_str, calc_Excel_val (next_day_dt),
                next_month_str, calc_Excel_val (next_month_dt))
        
        cursor.execute (query, args)
        conn.commit()    
    except Error as e:
        print(e)
        
    finally:
        print "Closing connection"
        cursor.close()
        conn.close()

    
# Takes a datetime object and returns the yyyy/mm/dd string
def date_obj_str (dt):
    return  (dt.__str__()).split(' ')[0]

# Calculate the Excel date value for the inputted datetime object
def calc_Excel_val (dt):
    Excel_ref_dt = datetime(1900, 1, 1)
    return (dt - Excel_ref_dt).days

#-----------------------------------------------------------------------------
# Updates INVCODE field in month_table
def update_INVCODE():
    
    db_config = read_db_config ()
    if len(db_config) == 0:
        sys.exit()
    try:
        conn = MySQLConnection (**db_config)
        if conn.is_connected():
            print "Connected to MySQL database"

        cursor = conn.cursor()

        query = """
                   UPDATE month_temp, invoice_codemap
                   SET month_temp.INV_CODE = CONCAT (month_temp.BillingCode,
                   ':', invoice_codemap.Invoice_Code)
                   WHERE month_temp.Invoice_Date = invoice_codemap.Invoice_Date
                """ 
        args = ()
        
        cursor.execute (query, args)
        conn.commit()    
    except Error as e:
        print(e)
        
    finally:
        print "Closing connection"
        cursor.close()
        conn.close()

# Inserts month_temp values into invoices table
def insert_new_invoices ():
    
    db_config = read_db_config ()
    if len(db_config) == 0:
        sys.exit()
    try:
        conn = MySQLConnection (**db_config)
        if conn.is_connected():
            print "Connected to MySQL database"

        cursor = conn.cursor()

        query = """
                   INSERT INTO invoices
                   SELECT * FROM month_temp
                """ 
        args = ()
        
        cursor.execute (query, args)
        conn.commit()    
    except Error as e:
        print(e)
        
    finally:
        print "Closing connection"
        cursor.close()
        conn.close()

def drop_created_tables ():
    db_config = read_db_config ()
    if len(db_config) == 0:
        sys.exit()
    try:
        conn = MySQLConnection (**db_config)
        if conn.is_connected():
            print "Connected to MySQL database"

        cursor = conn.cursor()

        query = """
                   DROP TABLE month_temp;
                   DROP TABLE invoice_codemap
                """ 
        args = ()
        
        for result in cursor.execute (query, args, multi=True):
            pass

    except Error as e:
        print(e)
        
    finally:
        print "Closing connection"
        cursor.close()
        conn.close()

def create_output_file ():
    filename = 'Quincy_invoices.csv'

    db_config = read_db_config ()
    if len(db_config) == 0:
        sys.exit()
    try:
        conn = MySQLConnection (**db_config)
        if conn.is_connected():
            print "Connected to MySQL database"

        cursor = conn.cursor()

        query = """
                   (SELECT 'INV_CODE', 'Invoice_Date', 'Billed_Month',
                    'Service_Month', 'Payee', 'Firm_Code', 'BillingCode',
                    'Attributable', 'Description', 'Rate', 'Commission',
                    'Percentage', 'Status')
                   UNION
                   (SELECT * FROM invoices
                   WHERE Status = 'Unpaid'
                   INTO OUTFILE '/home/osboxes/Quincy/Quincy_invoices.csv'
                   FIELDS ENCLOSED BY '"'
                   TERMINATED BY ','
                   LINES TERMINATED BY '\n')
                """ 
        args = (filename)        
        cursor.execute (query, args)

    except Error as e:
        print(e)
        
    finally:
        print "Closing connection"
        cursor.close()
        conn.close()
        
def main():
    
    create_init_table()
    modify_table_invoice_form()
    add_firm_code()

    month_num = raw_input ("Please enter month number to update invoice " \
                           "table:\n")
    try:    
        while (int(month_num) < 1 or int(month_num) > 12):
            month_num = raw_input ( "Not a valid entry. " \
                                "Please enter month number\n")
    except Exception:
        print "Not an integer. System exit"
        sys.exit()
    
    update_date_info (month_num)
    invoice_date_exceptions (month_num)    
    service_month_exceptions (month_num)
    create_invcode_table(month_num)
    update_invoice_code_table (month_num)
    update_INVCODE()
    insert_new_invoices ()
    drop_created_tables ()    
    create_output_file ()

# main()
create_output_file ()
