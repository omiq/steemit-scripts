
from steem import Steem
s = Steem()

from steem.transactionbuilder import TransactionBuilder
from steembase import operations

import time, random, os

rposts = s.get_account_history('makerhacks',-1,10000)

total = 0
for post in rposts:

    operation =  post[1]['op'][0]
    if operation == "transfer":
        if post[1]['op'][1]['from'] == "makerhacks" and not post[1]['op'][1]['to'] == "themarkymark":
            print( post[1]['op'][1]['to'] + "\t\t\t" + str( post[1]['op'][1]['amount'] ))
            total = total + float(post[1]['op'][1]['amount'].replace(' SBD',''))


print ("\n\n" + str(total) + " SBD \n\n\n")
