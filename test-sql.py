import os
import sys
from time import sleep
import pyodbc
from datetime import datetime, timedelta
from dateutil import tz

from_zone = tz.gettz('UTC')
to_zone = tz.gettz('America/Denver')


def get_connection():

    db_host = 'vip.steemsql.com'
    db_name = 'DBSteem'
    db_user = os.environ['DBU']
    db_password = os.environ['DBPASS']
    connection_string = 'Driver={ODBC Driver 13 for SQL Server};Server=' + db_host + ';Database=' + db_name + ';UID=' + db_user + ';PWD=' + db_password + ';'
    connection = pyodbc.connect(connection_string)
    return connection


def get_latest(connection, keyword):

    cursor = connection.cursor()
    sql_command = "select top (1) id, title, " \
                 "created, '@'+author+'/'+permlink as link " \
                 " from Comments " \
                 " where depth=0 " \
                 "      and body_language like '%language\":\"en%' " \
                 "      and title like '%{}%' " \
                 " order by ID desc;".format(keyword)

    result = cursor.execute(sql_command)
    result = result.fetchmany(1)
    return result


connection = get_connection()

lastresult = 0
keyword = sys.argv[1]
while 1:
    result = get_latest(connection, keyword)
    if int(result[0][0]) > lastresult:
        os.system('clear')
        created = result[0][2] - timedelta(hours=7)
        print("ID: {}\tTitle: {}\tCreated: {}\nLink: {}".format(result[0][0], result[0][1], created, result[0][3]))
    lastresult = int(result[0][0])

    sleep(1)

connection.close()
