# first, we initialize Steem class
from steem import Steem
s = Steem()

import datetime 
from rfeed import *

posts = s.get_blog( 'makerhacks',0,5 )

oitems = []

for post in posts:
        ilink = "https://steemit.com/steemit" + post['comment']['parent_permlink'] + "/@makerhacks/" + post['comment']['permlink']
        ititle = post['comment']['title']
        idescription = post['comment']['body'].split( "\n" )[0]
        iauthor = post['comment']['author']
        icreated = post['comment']['created']

        oitems.append( Item(
            title = ititle,
            link = ilink, 
            description = idescription,
            author = iauthor,
            guid = Guid(ilink) ) )

feed = Feed(
    title = "RSS Feed",
    link = "https://www.makerhacks.com/",
    description = "RSS 2.0 feed",
    language = "en-US",
    lastBuildDate = datetime.datetime.now(),
    items = oitems)

print(feed.rss())
