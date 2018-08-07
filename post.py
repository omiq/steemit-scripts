import os
import sys
import time, random, os
from steem import Steem
from steem.transactionbuilder import TransactionBuilder
from steembase import operations
s = Steem()

# markdown
from markdown2 import Markdown
md = Markdown()


def submit_post(title, tags, body, author):

    permlink_title = ''.join(e for e in title if e.isalnum()).lower()
    permlink = "{}-%s%s".format(permlink_title) % (time.strftime("%Y%m%d%H%M%S"), random.randrange(0, 9999, 1))

    try:
        s.post(title, body, author, permlink, None, None, None, None, tags, None, True)
        print("Submitted post: {}".format(permlink))
    except Exception as error:
        print(repr(error))

    return permlink


def run():

    # credentials
    inFile = open('/home/chrisg/mailgun-api.txt', 'r')
    api_key = inFile.readline().rstrip()
    password = inFile.readline().rstrip()

    # get authenticated steem obj
    s.wallet.unlock(pwd=password)

    # get post params
    author = sys.argv[1]
    title  = sys.argv[2]
    tags   = sys.argv[3]
    body   = sys.argv[4].replace('\\n', os.linesep)

    permlink = ""
    permlink = submit_post(title, tags, body, author)
    print(permlink)


if __name__ == '__main__':
        run()