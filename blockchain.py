from steem import Steem
from steem.blockchain import Blockchain
from steem.post import Post
import json
import datetime
import time

from steem import Steem
from steem.blockchain import Blockchain
from steem.post import Post
import json
import datetime
import http.client

import sqlite3
from sqlite3 import Error

# we want to restart after a set period 
EXECUTIONSTART = time.time()
MAXEXECUTION = 60 * 60


# connect to the supplied database
def create_connection(db_file):
    """ create a database connection to a SQLite database """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

# web hook URL for Discord
url = "https://discordapp.com/api/webhooks/412417201216421888/Qr0EYGw7tEN6VsPL6mmx_w0DmPeP5V4YC1rN0TNitUTObX9A4SOUGWwfF5R0UxWACXcK"

# retrieve keywords in keyword order
def get_records():

    # get db connection
    conn = create_connection("../keywords-sqlite.db")

    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM keywords ORDER BY keyword ASC;''')

    list = []
    for row in cursor:
    # row['name'] returns the name column in the query, row['email'] returns email column.
        list.append( row['keyword'] )
    conn.close()
    return list


def send(message, webhook):
 
    conn = http.client.HTTPSConnection("discordapp.com")
 
    payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"content\"\r\n\r\n" + message + "\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"
 
    headers = {
        'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
        'cache-control': "no-cache",
        }
 
    conn.request("POST", webhook, payload, headers)
 
    res = conn.getresponse()
    data = res.read()
 
    print(data.decode("utf-8"))


def converter(object_):
    if isinstance(object_, datetime.datetime):
        return object_.__str__()

def stream_blockchain():
    blockchain = Blockchain()
    stream = map(Post, blockchain.stream(filter_by=['comment']))


    while True:
        try:
            for post in stream:

                #print("Diff {}".format( (EXECUTIONSTART + MAXEXECUTION) - time.time() )) 

                # did we go too long?
                if time.time() > (EXECUTIONSTART + MAXEXECUTION):
                    print("Diff {}".format( (EXECUTIONSTART + MAXEXECUTION) - time.time() ))
                    exit()
  
                # do the thing
                tags = post["tags"]
                if post.is_main_post(): # and "utopian-io" in tags:
                    author = post["author"]
                    title = post["title"]
                    body = post["body"]

                    haystack = ""
                    haystack = author + " " + title #+ " " + body

                    # this could take a long time as the list grows
                    my_keywords = get_records()
                    
                    for this_word in my_keywords:
                        if haystack.lower().find( this_word ) > 0:
                            thislink = "https://steemit.com" + post.url
                            msg = ("***{}*** found! - *{}* posted {}\n{}".format(this_word, author, title, thislink ))
                            send( msg, url)
        except Exception as error:
            # print(repr(error))
            continue


# ok start!
stream_blockchain()
