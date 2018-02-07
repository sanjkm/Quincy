import mysql.connector
from mysql.connector import MySQLConnection, Error
from mysql_dbconfig import read_db_config
import sys

def connect():
    """ Comment testing """

    db_config = read_db_config ()
    if len(db_config) == 0:
        sys.exit()
    try:
        print "Here we go"
        conn = MySQLConnection (**db_config)
        if conn.is_connected():
            print "Connected to MySQL database"
        
        
        clean_LB_paid_table (conn)
        convert_csv_table (conn)
        print "Conversion done"
        update_invoices_table (conn)
        create_unpaid_csv (conn)
        unpaid_invoice_summary (conn)
        
    except Error as e:
        print(e)
        
    finally:
        print "Closing connection"
        conn.close()


def clean_LB_paid_table (conn):
    cursor = conn.cursor()
    query = "DELETE FROM LB_paid_list"
    args = ()
    cursor.execute(query, args)
    conn.commit()
    cursor.close()
        
# Converts the LB paid list from a csv into a data table
def convert_csv_table (conn):

    cursor = conn.cursor()

    query = "LOAD DATA INFILE '/home/osboxes/Quincy/LB_paid.csv' " \
            "INTO TABLE LB_paid_list " \
            "FIELDS TERMINATED BY ',' " \
            "LINES TERMINATED BY '\n' " \
            "IGNORE 1 ROWS"
    args = ()

    cursor.execute (query, args)
    conn.commit()
    cursor.close()

# Updates invoice table with the paid list sent from LB
def update_invoices_table (conn):
    cursor = conn.cursor()

    query = "UPDATE invoices t1 " \
            "INNER JOIN LB_paid_list t2 " \
            "ON (t1.BillingCode=t2.BillingCode) AND " \
            "(t1.Description=t2.Description) AND " \
            "(t1.Billed_Month=t2.Billed_Month) " \
            "SET t1.Status = t2.Status"
    args = ()

    cursor.execute(query, args)
    conn.commit()
    cursor.close()

def create_unpaid_csv (conn):
    cursor = conn.cursor()

    query = """
           (SELECT 'INV_CODE', 'Invoice_Date', 'Billed_Month',
            'Service_Month', 'Payee', 'Firm_Code', 'BillingCode',
            'Attributable', 'Description', 'Rate', 'Commission',
            'Percentage', 'Status')
           UNION
           (SELECT * FROM invoices
           WHERE Status = 'Unpaid'
           INTO OUTFILE '/home/osboxes/Quincy/current_unpaid_invoices.csv'
           FIELDS ENCLOSED BY '"'
           TERMINATED BY ','
           LINES TERMINATED BY '\n')
        """
    args = ()

    cursor.execute (query, args)

# Create table summarizing the unpaid invoices by billing codes
# Output table into csv file
def unpaid_invoice_summary (conn):
    cursor = conn.cursor()

    query = """
           (SELECT 'BillingCode', 'Count', 'TotalOwed',
            'Earliest')
           UNION
           (SELECT BillingCode, Count(*), SUM(RATE), MIN(Service_Month)
           FROM invoices
           WHERE Status = 'Unpaid'
           GROUP BY BillingCode
           INTO OUTFILE '/home/osboxes/Quincy/unpaid_invoice_summary.csv'
           FIELDS ENCLOSED BY '"'
           TERMINATED BY ','
           LINES TERMINATED BY '\n')
        """
    args = ()

    cursor.execute (query, args)


def main():
    
    connect()

main()

