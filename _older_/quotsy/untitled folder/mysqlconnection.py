""" Import Oracle's python connector for MySQL """
import mysql.connector
import collections

def _convert(data):
    if isinstance(data, basestring):
        return str(data)
    elif isinstance(data, collections.Mapping):
        return dict(map(_convert, data.iteritems()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(_convert, data))
    else:
        return data

# create a class that will give us an object we can use to connect to database
class MySQLConnection(object):
    # init method with configurations
    def __init__(self, db):
        """ BEGIN DATABASE CONFIGURATIONS """
        self.config = {
            'user': 'root',
            'password': 'root',
            'database': db,  #db is argument in init
            'host': 'localhost',
        }
        self.conn = mysql.connector.connect(**self.config)

    """ BELOW ARE CUSTOM FUNCTIONS BUILT TO WORK AROUND ALCHEMY """
    """
    fetch function should be used for queries that return multiple rows
    Rows are returned in a list of tuples w/ each tuple corresponding to a row
    """
    # begin fetch method
    def fetch(self, query):
        cursor = self.conn.cursor(dictionary=True)
        cursor.execute(query)
        data = list(cursor.fetchall())
        cursor.close()
        return _convert(data)

    """
    run_mysql_query function should be used for INSERT/UPDATE/DELETE queries
    returns the number of rows affected
    """
    # begin change method
    def change(self, query):
        cursor = self.conn.cursor(dictionary=True)
        data = cursor.execute(query)
        self.conn.commit()
        cursor.close()
        return data

# call this module method in server.py (make sure to include db name when calling)
def MySQLConnector(db):
    return MySQLConnection(db)
