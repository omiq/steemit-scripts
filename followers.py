import math
from steem.account import Account

from steem import Steem

import sys


s = Steem()
account = sys.argv[1]

for following in Account(account).get_following():

    rep = int( Account(following)['reputation'] )
    fol = int( s.get_follow_count( following )['follower_count'] )

    if rep > 0:
        rep = round(((math.log(rep,10))-9)*9,2)+25
    print ( '\n' + following + ':' + str( rep ) )

    if fol < 1000:
        if account in Account(following).get_following():
            print  ('Follows back: Yes')
        else:
            print  ('Follows back: No')
    else:
        print(str(fol) + " followers!")
