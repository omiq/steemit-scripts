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


# retrieve steemians for user
def get_articles(conn,user):

    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('''select * from articles where blog = ? order by added_date desc;''',(user,))

    for row in cursor:
    # row['name'] returns the name column in the query, row['email'] returns email column.
        print('{0} link:{1} added: {2}'.format(row['blog'], row['link'], row['added_date']))
    conn.close()

# get db connection
conn = create_connection("../articles-sqlite.db")

blog="makerhacks"
get_articles(conn,blog)