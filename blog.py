# first, we initialize Steem class
from steem import Steem
s = Steem()

import pprint

posts = s.get_blog( 'makerhacks',0,5 )

pp = pprint.PrettyPrinter( indent=8 )

pp.pprint( posts[0]['comment'] )

#for post in posts:
#	print( "\n* <a href=\"/" + post['comment']['parent_permlink'] + "/@makerhacks/" + post['comment']['permlink'] + "\">"  + post['comment']['title'] + "</a>" )
