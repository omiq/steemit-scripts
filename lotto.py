import sys
import random
from steem import Steem

user = sys.argv[1]

steem = Steem()

history = steem.get_account_history(user, index_from=-1, limit=2000)

list = []
for entry in history:

    if entry[1]['op'][0] == 'transfer' and entry[1]['op'][1]['from'] != user:

        list.append(entry[1]['op'][1]['from'])

for winner in range(10):
    print(list[random.randint(0,len(list))])
