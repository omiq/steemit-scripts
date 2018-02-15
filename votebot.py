import os
import sys
import datetime
import subprocess
import requests
import http.client
import sqlite3
from sqlite3 import Error
from string import Template 
from steem.account import Account
import steemfunc

from steem import Steem
s = Steem()

from steem.transactionbuilder import TransactionBuilder
from steembase import operations
from steem.post import Post

import time, random

# colors
WHITEONBLUE = "\033[1;37;44m" 
BRIGHTGREENONBLACK = "\033[1;32;40m" 
GREENONBLACK = "\033[0;32;40m" 
GREENONGREY = "\033[1;32;100m" 
RESETCOLOR = "\033[0m"

# send via discord
def send_message(who,message):
    
    webhook = "https://discordapp.com/api/webhooks/412417201216421888/Qr0EYGw7tEN6VsPL6mmx_w0DmPeP5V4YC1rN0TNitUTObX9A4SOUGWwfF5R0UxWACXcK"
 
    conn = http.client.HTTPSConnection("discordapp.com")
 
    payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"content\"\r\n\r\n" + message + "\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"
 
    headers = {
        'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
        'cache-control': "no-cache",
        }
 
    conn.request("POST", webhook, payload, headers)
 
    res = conn.getresponse()
    data = res.read()


# send via Mailgun
def send_mailgun_message(who,msg):
    return requests.post(
        "https://api.mailgun.net/v3/chrisg.mailgun.org/messages",
        auth=("api", api_key),
        data={"from": "Steem Vote Bot <steem@chrisg.mailgun.org>",
              "to": ["chris@omiq.com"],
              "subject": "Vote: " + who,
              "text": msg})



# connect to the supplied database
def create_connection(db_file):
    """ create a database connection to a SQLite database """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

# retrieve steemians for user
def get_steemians(conn, user):

    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('''SELECT user, steemian, added_date FROM steemians WHERE user = ?;''',(user,))

    rows = []
    for row in cursor:
    # row['name'] returns the name column in the query, row['email'] returns email column.
        print('{} added {} on {}'.format( row['user'],row['steemian'], row['added_date'] ))
        rows.append(row['steemian'] )
    
    return rows

# get author most recent post
def getlast( author ):

    rposts = s.get_blog( author,0,5 )

    permlink = ""
    count = 0

    if (len(rposts) > 0 ):
        permlink = rposts[count]['comment']['permlink']
        this_author = rposts[count]['comment']['author']

        # print(this_author)
        while this_author != author:

            count+=1
            this_author = rposts[count]['comment']['author']

        return rposts[count]
    else:
        return []

def checkvotes( post, account ):

    result = False

    post_votes = post['active_votes']
    for upvoter in post_votes:
        if upvoter['voter'] == account:
            result = True

    return result

def get_vp( account ):
    SP = steemfunc.calculateSP(account)
    #print('Steem Power:', int(SP), 'SP')
    VP = steemfunc.getactiveVP(account)
    #print('Voting Power:', int(VP), '%')
    VoteValue = steemfunc.getvotevalue(SP, VP, 100)
    #print('Max vote value with Steem Power and Voting Power above:', round(VoteValue,3), 'SBD')
    VotingWeight = steemfunc.getvoteweight(SP, VoteValue, VP)
    #print('Voting Weight needed:', int(round(VotingWeight,0)), '%')
    return VP

def vote_last_post( user, author, weight):

    # change to this account
    voter = s.get_account(user)

    lastpost = getlast( author )
    #weight = 50

    # do they have posts?
    if len(lastpost) > 0: 

        # let's not upvote comments
        if lastpost['comment']['title'] != "":
            permlink = "@" + author + "/" + lastpost['comment']['permlink']
            thispost = Post(permlink)

            # output the result to screen
            out = Template( "Vote on $permlink with $weight % by $account " )
            output = out.safe_substitute( { 'permlink': permlink, 'weight': weight, 'account': user } )
            print( output )

            voted = checkvotes( thispost, user )

            if voted != True:
                try:
                    s.vote( permlink, weight, user )
                    send_message( user + " voted on " + author, output )
                except:
                    print( "Oops, error - voting power probably too low!")
            else:
                print("-- Oops, " + user + " already voted on that one")

# API KEY
inFile = open('/home/chrisg/mailgun-api.txt', 'r')
api_key = inFile.readline().rstrip()

# Password
password = inFile.readline().rstrip()

nodes = ['rpc.buildteam.io']
steem=Steem(nodes)
steem.wallet.unlock(pwd = password)

# Close file
inFile.close()

# get db connection
conn = create_connection("/home/chrisg/tofollow-sqlite.db")

# Iterate accounts/users and authors/steemians
steemusers = ['makerhacks', 'loveyourstyle', 'davincibot', 'geekahol', 'builduino','canuckbot']

# right now same weight for everyone
weight = int(sys.argv[1]) 

for user in steemusers:

    # next user
    print( "\n\n{}{} to vote on next:{}".format(BRIGHTGREENONBLACK,user,RESETCOLOR))

    # calculate voting power
    account = Account( user )
    vp = get_vp( account )
    rows = []
    if vp > 70:
        del rows[:]
        rows = get_steemians(conn,user)
        print(rows)

        for author in rows:
            vote_last_post( user, author, weight )
            time.sleep(10)

    else:
        print( "{}Vote Power for {} is only {}, waiting ...{}\n\n".format(WHITEONBLUE,user,vp,RESETCOLOR))