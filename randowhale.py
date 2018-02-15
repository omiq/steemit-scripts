import json
import datetime
import http.client

import math
from steem.account import Account

from steem import Steem

import sys

# web hook URL for Discord
url = "https://discordapp.com/api/webhooks/412417201216421888/Qr0EYGw7tEN6VsPL6mmx_w0DmPeP5V4YC1rN0TNitUTObX9A4SOUGWwfF5R0UxWACXcK"

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

s = Steem()
sleeping = Account("randowhale")['json_metadata']['config']['sleep']

if sleeping:
    do=False
else:
    print("Awake!")
    send("***@randowhale is awake!***",url)


