#!/usr/bin/env python3

'''
		https://api.imgur.com/endpoints/image
'''

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
        cur.execute(sql, (blog, extlink, html, datetime.now()) )
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
        print('{0} link:{1} added: {2}'.format(row['blog'], row['link'], row['added_date']))
    conn.close()


import metadata_parser
import configparser
import urllib.request
import requests
import os
import glob
from PIL import Image
import ssl

## DANGER! NOT ADVISED!
ssl._create_default_https_context = ssl._create_unverified_context

from datetime import datetime

album = None # You can also enter an album ID here


def upload_image(client, image_path):
	'''
		Upload a picture 
	'''

	# Here's the metadata for the upload. All of these are optional, including
	# this config dict itself.
	config = {
		'album': album,
		'name':  'Thumbnail',
		'title': 'Thumbnail',
		'description': 'Thumbnail uploaded on {0}'.format(datetime.now())
	}

	image = client.upload_from_path(image_path, config=config, anon=False)


	return image



def get_configuration():
    config = configparser.ConfigParser()
    config.read('auth.ini')
    return config

def thum(infile):

    # convert to RGB
    im = Image.open(infile).convert('RGB')

    # convert to thumbnail image
    im.thumbnail((300, 300), Image.ANTIALIAS)

    # suffix thumbnail file with _THUMB
    sfile = infile + "_THUMB"
    im.save( sfile, "JPEG")

    # delete converted file
    os.remove(infile)
    return sfile


# file to upload
blog = sys.argv[1]	
articlelink = sys.argv[2]
meta = []

try:
    page = metadata_parser.MetadataParser(url=articlelink,search_head_only=-1)
    meta = page.metadata
    imgurl = meta['meta']['og:image']
except:
    imgurl = "https://steemit-production-imageproxy-upload.s3.amazonaws.com/DQmfTnQ1gJ5uQU3CFR3Zyg847buY8oVKWNHYoyKkJDnb7NJ"


lfile = requests.get(imgurl)
file, headers = urllib.request.urlretrieve( imgurl )

# thumbnail the effer
file = thum(file)

from imgurpython import ImgurClient
# Note since access tokens expire after an hour, only the refresh token is required (library handles autorefresh)

config = get_configuration()
client_id = config.get('credentials', 'client_id')
client_secret = config.get('credentials', 'client_secret') 
access_token = config.get('credentials', 'access_token')
refresh_token = config.get('credentials', 'refresh_token')

client = ImgurClient(client_id, client_secret, access_token, refresh_token)

image = upload_image(client, file)

if len(meta) > 0:
    desc = meta['meta']['og:description'].replace( "… by ", "<br>-- @")

    output = ""
    output+=("\n\n\n")
    output+=("<h2><a href=\"{1}\">{0}</a></h2>".format(meta['meta']['og:title'],articlelink))
    output+=("\n<div class=\"pull-left\">\n{0}\n".format(image['link']))
    output+=("</div><blockquote>\n{0}\n</blockquote>".format(desc))
    output+=("<p  style=\"clear: both; \" /><br  style=\"clear: both;\" /></p><p  style=\"clear: both; \" /><br  style=\"clear: both;\" />\n\n\n...Check it out!...\n\n<h3><a href=\"{0}\">Read More</a></h3>".format(articlelink))
    output+=("<p  style=\"clear: both;\"> </p><p  style=\"clear: both;\"> </p><p><hr>")
    output+=("\n\n\n")

else:
    output = "Can not process added link: {}".format(articlelink)

#print(output)

# DATABAAAASSSSSEEEE

# get db connection
conn = create_connection("../articles-sqlite.db")

sql_create_table = """ CREATE TABLE IF NOT EXISTS articles (
                                        id integer PRIMARY KEY,
                                        blog text NOT NULL,
                                        link text NOT NULL, html text,
                                        added_date text
                                    ); """

exec_sql(conn,sql_create_table)

print( create_entry(conn, blog, articlelink, output) )
get_articles(conn,blog)
