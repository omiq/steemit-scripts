from steem import Steem
from steem.account import Account
from steem.post import Post
from steem.amount import Amount
from dateutil.parser import parse
from datetime import datetime, timedelta

steem = Steem()
account = "makerhacks"
total = 0

# Get days since account creation
created = parse(Account(account)["created"]).date()
today = datetime.today().date()
days = today - created

# Create dictionary
dates = {}
for day in range(days.days + 1):
    dates[str(created + timedelta(days=day))] = 0

# Iterate over all blog posts
print("\n\n  Date      \t\tPayout SBD\n")
print("  ==========\t\t==============\n\n")
post_limit = 500

if post_limit > 0:
    for post in steem.get_blog(account, 0, post_limit):
        post = Post(post["comment"])
        if post.is_main_post() and post["author"] == account:
            post_date = str(post["created"].date())
            payout=(( Amount(post["pending_payout_value"]).amount * 0.75) /2)
            if payout == 0:
                payout = (Amount(post["total_payout_value"]).amount - Amount(post["curator_payout_value"]).amount)
            dates[post_date] += payout
            permlink = post['permlink']
            total = total + payout

            print("  "  + post_date + "\t\t" + str(payout) + "\t\t\t\t" + permlink )


print("\n\n\n============\n" + str(total) + " SBD\n\n\n")

