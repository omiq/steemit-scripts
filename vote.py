from contextlib import suppress

from steem.blockchain import Blockchain
from steem.post import Post

from steem import Steem
s = Steem()


# steem.vote(permlink, weight, account)

def run():
    # upvote posts with 30% weight
    upvote_pct = 30
    whoami = 'makerhacks'

    # stream comments as they are published on the blockchain
    # turn them into convenient Post objects while we're at it
    b = Blockchain()
    stream = map(Post, b.stream(filter_by=['comment']))

    for post in stream:
        if post.json_metadata:
            mentions = post.json_metadata.get('users', [])

            # if post mentions more than 10 people its likely spam
            if mentions and len(mentions) < 10:
                post.upvote(weight=upvote_pct, voter=whoami)

if __name__ == '__main__':
    with suppress(KeyboardInterrupt):
        run()
