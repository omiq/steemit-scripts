import sys
import time
from steem import Steem

inFile = open('/home/chrisg/mailgun-api.txt', 'r')
api_key = inFile.readline().rstrip()

amount = 0
author = ""

# Password
password = inFile.readline().rstrip()

nodes = ['rpc.buildteam.io']
s = Steem()

try:
    s.wallet.unlock(pwd = password)
except Exception as error:
    print(repr(error))
    quit()

from steem.transactionbuilder import TransactionBuilder
from steembase import operations

import time, random, os



def buy_upvote( author, upvote_bot, amount, permlink) :
    
    transfers =[{
        'from': author,
        'to': upvote_bot,
        'amount': '{0:.3f} SBD'.format(amount),
        'memo': 'https://steemit.com/@{}/{}'.format(author, permlink)
    }]

    print("\n\n")
    print("Buying " + upvote_bot + " " + str(amount) + " vote for author " + author + "\n and permalink " + permlink)
    print("\n\n")

    tb = TransactionBuilder()
    operation = [operations.Transfer(**x) for x in transfers]
    tb.appendOps(operation)
    tb.appendSigner(author, 'active')
    tb.sign()

    try:
        tx = tb.broadcast()
        print ("** Vote success")
    except Exception as error:
        print(repr(error))



def getlast(author):
    rposts = s.get_blog( author,0,5 )

    permlink = ""
    count = 0
    thisauthor = rposts[count]['comment']['author']
    while thisauthor != author:
        count+=1
        thisauthor = rposts[count]['comment']['author']
        permlink = rposts[count]['comment']['permlink']


    return rposts[count]['comment']['permlink']




# smartmarket and minnowbooster are the safest
upvote_bot = 'minnowbooster'
amount = float(sys.argv[1])
author = sys.argv[2]
numvotes = int(sys.argv[3])
permlink = sys.argv[4]



for x in range(0, numvotes ):
    buy_upvote(author, upvote_bot, amount, permlink)
    if numvotes > 1: time.sleep(20)


