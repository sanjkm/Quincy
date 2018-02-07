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
        

    except Error as e:
        print(e)
        
    finally:
        print "Closing connection"
        conn.close()
        
def main():
    
    connect()

main()

