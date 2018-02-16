import os
import sys
import json
from steem import Steem
from steem.amount import Amount
from steem.dex import Dex
from steem.account import Account
import locale
import requests

WHITEONBLUE = "\033[1;37;44m" 
GREENONBLACK = "\033[0;32;40m" 
GREENONGREY = "\033[1;32;100m" 

# USD
locale.setlocale( locale.LC_ALL, '' )


def get_steem_price():

    r = requests.get("https://api.coinmarketcap.com/v1/ticker/steem/?convert=USD")

    result = r.json()

    return result['price_usd']


def get_sbd_price():
    r = requests.get("https://api.coinmarketcap.com/v1/ticker/steem-dollar/?convert=USD")

    result = r.json()

    return result['price_usd']


def rewards(USERNAME):

    print()
    print(WHITEONBLUE + " " + USERNAME.upper() + " ACCOUNT " + GREENONBLACK)
    print()

    acc = steem.get_account(USERNAME)
    account = Account(USERNAME)

    reward_SBD = acc["reward_sbd_balance"]
    reward_SP  = acc["reward_vesting_steem"]
    print("\n\nYour current rewards: {} and {} POWER".format(reward_SBD, reward_SP))
    
    allSP = float(acc.get('vesting_shares').rstrip(' VESTS'))
    delSP = float(acc.get('delegated_vesting_shares').rstrip(' VESTS'))
    recSP = float(acc.get('received_vesting_shares').rstrip(' VESTS'))
    activeSP = account.converter.vests_to_sp(allSP - delSP + recSP)

    print("\n\nSTEEM POWER\t{:0.6f}".format( activeSP ))

    sbd_balance = Amount(acc["sbd_balance"]).amount
    lowest_ask = float(steem.get_ticker()["lowest_ask"])
    print("\n\nSBD BALANCE\t{:0.6f}".format( sbd_balance ))
    print("\n\nSTEEMSBD:\t{:0.6f}".format( lowest_ask, ) )

    sbdbase = float(Amount(steem.steemd.get_feed_history()['current_median_history']['base']).amount)

    print("\n\nMARKET:")
    print("\nSTEEMUSD:\t{}".format(locale.currency(get_steem_price())))
    print("\nSBDUSD:\t{}".format(locale.currency(get_sbd_price())))

    print("\n\nINTERNAL:")
    print("\n\nSTEEMUSD:\t{}".format( locale.currency(sbdbase) ) )
    
    sbdusd = sbdbase / lowest_ask
    print("\n\nSBDUSD:\t{}".format( locale.currency(sbdusd) ) )
    
    print("\n\nSBD USD BALANCE\t\t{}".format( locale.currency(sbd_balance * sbdusd )))
    print("\n\nSP USD BALANCE\t\t{}".format( locale.currency(activeSP * sbdbase )))
    print("\n\n{}TOTAL BALANCE\t\t{}{}\n\n\n".format(GREENONGREY, locale.currency((activeSP * sbdbase )+(sbd_balance * sbdusd )),GREENONBLACK))

if __name__ == '__main__':
    steem = Steem()
    rewards(sys.argv[1])
    