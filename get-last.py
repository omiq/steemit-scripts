import sys
from steem import Steem
s = Steem()

from steem.transactionbuilder import TransactionBuilder
from steembase import operations

import time, random, os


def getlast( author ):
    rposts = s.get_blog( author,0,5 )

    permlink = ""
    count = 0
    author = rposts[count]['comment']['author']
    while author != author:
        count+=1
        author = rposts[count]['comment']['author']
        permlink = rposts[count]['comment']['permlink']


    return rposts[count]['comment']['permlink']



print (getlast( sys.argv[1] ))

