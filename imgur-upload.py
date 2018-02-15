#!/usr/bin/env python3

'''
		https://api.imgur.com/endpoints/image
'''

import sys
import configparser

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

# file to upload	
file = sys.argv[1]

from imgurpython import ImgurClient
# Note since access tokens expire after an hour, only the refresh token is required (library handles autorefresh)

config = get_configuration()
client_id = config.get('credentials', 'client_id')
client_secret = config.get('credentials', 'client_secret') 
access_token = config.get('credentials', 'access_token')
refresh_token = config.get('credentials', 'refresh_token')

client = ImgurClient(client_id, client_secret, access_token, refresh_token)

image = upload_image(client, file)

print("URL:{0}".format(image['link']))