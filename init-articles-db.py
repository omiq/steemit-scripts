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
def create_entry(conn, blog, extlink, html ):
 
    sql = ''' INSERT INTO articles ( blog, link, html, added_date)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()

    try:
        cur.execute(sql, (blog, extlink, html, datetime.datetime.now()) )
        conn.commit()
        return cur.lastrowid
    except Error as e:
        return e


# retrieve steemians for user
def get_articles(conn,user):

    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM articles WHERE blog = ?;''',(user,))

    for row in cursor:
    # row['name'] returns the name column in the query, row['email'] returns email column.
        print('{0} added: {1}'.format(row['link'], row['added_date']))
    conn.close()


# get db connection
conn = create_connection("../articles-sqlite.db")

sql_create_table = """ CREATE TABLE IF NOT EXISTS articles (
                                        id integer PRIMARY KEY,
                                        blog text NOT NULL,
                                        link text NOT NULL, html text,
                                        added_date text
                                    ); """

result = exec_sql(conn,sql_create_table)

if len(sys.argv) > 1:
    user = sys.argv[1]
    steemian = sys.argv[2]
    print( "Adding article: ")
    print( create_steemian(conn, blog, extlink, html) )
    get_articles(conn,user)

else:
    print("\n\nUsage:")
    print( "add-articles.py your_user link\n\n")

