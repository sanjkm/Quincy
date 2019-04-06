# query_delete.py
# Deletes records from tables within quincy database
# Records are determined from queries contained in
# inputted textfile, where filename is inputted as argument from command line

# Adds the parent directory to the path of this program
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) # contains module mysql_dbconfig
db_config_file = 'config.ini'
db_section = 'mysql'

from mysql_dbconfig import read_db_config

import mysql.connector
from mysql.connector import MySQLConnection, Error

from fill_query_list import fill_query_list

# If the field value begins with 'LIKE', then the equals in the query will
# be replaced with a LIKE statement
def check_for_LIKE (query_field_val):
    test_str = 'LIKE'
    
    if len(query_field_val) < (1 + len(test_str)):
        return 0
    if query_field_val[1:1+len(test_str)] == test_str:
        return 1
    return 0

# Executes the query defined by the field-attribute pairs contained in the
# inputted dictionary query_dict
def query_delete_execute (conn, query_dict):
    cursor = conn.cursor()
    table_name = query_dict['Table']
    query = "DELETE FROM " + table_name + " WHERE "
    index = 0
    for k in query_dict:
        if k == 'Table':
            continue

        # If field value begins with 'LIKE', then the query line is a
        # LIKE statement, not an equals
        # Query is modified appropriately
        if check_for_LIKE (query_dict[k]) == 1:    
            query_add = k + " LIKE '" + query_dict[k][6:] + " "

        else:
            query_add = k + "=" + query_dict[k] + " "
        if index > 0:
            query_add = "AND " + query_add
        query = query + query_add

        index+=1
    args = ()

    cursor.execute (query, args)
    conn.commit()

def main():
    if len(sys.argv) == 1:
        print "No input file entered"
        exit(1)
    
    db_config = read_db_config (parentdir + '/' + db_config_file, db_section)
    if len(db_config) == 0:
        sys.exit()
    try:
        conn = MySQLConnection (**db_config)
        if conn.is_connected():
            print "Connected to MySQL database"
            

        filename = sys.argv[1]
        # list of dictionaries containing query attributes
        query_list = fill_query_list(filename)
                    
        for query_dict in query_list:
            query_delete_execute (conn, query_dict)

    except Error as e:
        print(e)
        
    finally:
        print "Closing connection"
        conn.close()
    
main()
