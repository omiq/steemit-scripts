import sys
import datetime
import sqlite3
from sqlite3 import Error
 
 

# connect to the supplied database
def create_connection(db_file):
    """ create a database connection to a SQLite database """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

# execute supplied sql statements
def exec_sql(conn, in_sql):

    try:
        c = conn.cursor()
        c.execute(in_sql)
    except Error as e:
        print(e)

# add person to follow
def create_entry(conn, keyword, negative ):
 
    sql = ''' INSERT INTO keywords ( keyword, negative, added_date)
              VALUES(?,?,?) '''
    cur = conn.cursor()

    try:
        cur.execute(sql, (keyword, negative, datetime.datetime.now()) )
        conn.commit()
        return cur.lastrowid
    except Error as e:
        return e


# retrieve keywords in keyword order
def get_records(conn):

    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM keywords ORDER BY keyword ASC;''')

    for row in cursor:
    # row['name'] returns the name column in the query, row['email'] returns email column.
        print('{} added: {}'.format(row['keyword'], row['added_date']))
    conn.close()


# get db connection
conn = create_connection("../keywords-sqlite.db")

sql_create_table = """ CREATE TABLE IF NOT EXISTS keywords (
                                        id integer PRIMARY KEY,
                                        keyword text NOT NULL,
                                        negative text NOT NULL, 
                                        added_date text
                                    ); """

exec_sql(conn,sql_create_table)

if len(sys.argv) > 1:
    keyword = sys.argv[1]
    negative = sys.argv[2]
    html = ""
    print( "Adding keyword: ")
    print( create_entry(conn, keyword, negative ) )
    get_records(conn)


