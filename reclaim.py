import sys
import datetime
from steem import Steem
import subprocess
import requests
import http.client


# send via discord
def send_message(who,message):
    
    webhook = "https://discordapp.com/api/webhooks/412417201216421888/Qr0EYGw7tEN6VsPL6mmx_w0DmPeP5V4YC1rN0TNitUTObX9A4SOUGWwfF5R0UxWACXcK"
 
    conn = http.client.HTTPSConnection("discordapp.com")
 
    payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"content\"\r\n\r\n" + message + "\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"
 
    headers = {
        'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
        'cache-control': "no-cache",
        }
 
    conn.request("POST", webhook, payload, headers)
 
    res = conn.getresponse()
    data = res.read()


# send via Mailgun
def send_mailgun_message(who,msg):
    return requests.post(
        "https://api.mailgun.net/v3/chrisg.mailgun.org/messages",
        auth=("api", api_key),
        data={"from": "Steem Reclaim Bot <steem@chrisg.mailgun.org>",
              "to": ["chris@omiq.com"],
              "subject": "Steem Reclaim: " + sbd,
              "text": msg})



# API KEY
inFile = open('/home/chrisg/mailgun-api.txt', 'r')
api_key = inFile.readline().rstrip()

# Password
password = inFile.readline().rstrip()

# Close file
inFile.close()

# User list
steemuserlist = ['makerhacks', 'loveyourstyle', 'davincibot', 'geekahol', 'builduino','canuckbot']


def reclaim(steem, thisuser):
        if thisuser != "":
                user_info = steem.get_account(thisuser)

                reward_sbd = float(user_info['reward_sbd_balance'].split(' ')[0])
                reward_steem= float(user_info['reward_steem_balance'].split(' ')[0])
                reward_vesting = float(user_info['reward_vesting_balance'].split(' ')[0])
                reward_sp = float(user_info['reward_vesting_steem'].split(' ')[0])

                if reward_sbd > 0 or reward_steem > 0 or reward_vesting > 0:
                        steem.claim_reward_balance(account = thisuser)
                        msg = "{user} Claim rewards: {0} STEEM  {1} SBD {2} STEEM POWER".format(reward_steem, reward_sbd, reward_sp, user = thisuser)
                        print(msg)
                        send_message( thisuser, msg )
                else:
                        print("No rewards need to be claimed")


def main(argv=None):
        steem=Steem()
        steem.wallet.unlock(pwd = password)

        print(datetime.datetime.now())

        for thisuser in steemuserlist:

                print()
                print(thisuser)
                reclaim(steem, thisuser)

if __name__ == "__main__":
        sys.exit(main())
