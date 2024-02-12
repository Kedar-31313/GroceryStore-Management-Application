import mysql.connector
import datetime

__cnx = None

def get_sql_connection():
    print("Opening mysql connection")
    global __cnx

    if __cnx is None:
        __cnx = mysql.connector.connect(user='root', password='Kedar@31313', host='127.0.0.1', database='grocery_store')
    return __cnx