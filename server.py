from steem import Steem
s = Steem()

from flask import Flask
app = Flask(__name__)

@app.route('/')
def root_www():
    return 'BY YOUR COMMAND'

@app.route('/user/<username>')
def get_user(username):

    output = username + ' has ' + s.get_account(username)['sbd_balance'] 

    return output

