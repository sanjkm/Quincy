from ConfigParser import ConfigParser
import os

def read_db_config(filename='config.ini', section='mysql'):

    if os.path.isfile(filename):
    
        parser = ConfigParser()
        parser.read(filename)
    
        db = {}
        if section in parser.sections():
            items = parser.items(section)
            for item in items:
                db[item[0]] = item[1]
        else:
            raise Exception('{0} not found in the {1} file'.format(section,
                                                                       filename))
    else:
        print "File not found"
    return db
