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
def create_steemian(conn, user, steemian):
 
    sql = ''' INSERT INTO steemians (user, steemian, added_date)
              VALUES(?,?,?) '''
    cur = conn.cursor()

    try:
        cur.execute(sql, (user, steemian, datetime.datetime.now()) )
        conn.commit()
        return cur.lastrowid
    except Error as e:
        return e


# retrieve steemians for user
def get_steemians(conn,user):

    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('''SELECT steemian, added_date FROM steemians WHERE user = ?;''',(user,))

    for row in cursor:
    # row['name'] returns the name column in the query, row['email'] returns email column.
        print('{0} added: {1}'.format(row['steemian'], row['added_date']))
    conn.close()


# get db connection
conn = create_connection("../tofollow-sqlite.db")

sql_create_table = """ CREATE TABLE IF NOT EXISTS steemians (
                                        id integer PRIMARY KEY,
                                        user text NOT NULL,
                                        steemian text NOT NULL,
                                        added_date text
                                    ); """

result = exec_sql(conn,sql_create_table)

if len(sys.argv) > 1:
    user = sys.argv[1]
    steemian = sys.argv[2]
    print( "Adding follow: ")
    print( create_steemian(conn, user, steemian) )
    get_steemians(conn,user)

else:
    print("\n\nUsage:")
    print( "to-follow.py your_user person_to_follow\n\n")

