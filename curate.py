# first, we initialize Steem class
from steem import Steem
s = Steem()

# dates
import datetime
import sqlite3
from sqlite3 import Error

# our lightweight web server
from flask import request
from flask import Flask
app = Flask(__name__)

# markdown
from markdown2 import Markdown
md = Markdown()

# connect to the supplied database
def create_connection(db_file):
    """ create a database connection to a SQLite database """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

# for shell calls
import subprocess

# retrieve steemians for user
def get_articles(conn,user):

    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('''select * from articles where blog = ? order by added_date desc;''',(user,))
    output_html = ""

    for row in cursor:
    # row['name'] returns the name column in the query, row['email'] returns email column.
        output_html += row['html']
        output_html += "\n\n"
    conn.close()
    return output_html

# post footer
postfooter = "\n\n\n\n\n<hr><hr><center>https://steemitimages.com/DQmP22aDfrhrvSoPmFBpeeJezztADLzBbqoU14CGXNBbqmN/%40makerhacks-1.png</center>\n\n### Recently Popular\n"

rposts = s.get_blog( 'makerhacks',0,5 )

list = ""
for post in rposts:
    list+= "\n* <a href=\"/" + post['comment']['parent_permlink'] + "/@makerhacks/" + post['comment']['permlink'] + "\">"
    list+= post['comment']['title'] + "</a>" 

postfooter+=list + "</li></ul>"

# root
@app.route('/')
def root_www():

    return "Nothing to see yet"


@app.route('/blog/<blog>/', methods=["GET","POST"])
def get_blog_articles(blog):

    if request.method == "POST":
        link = request.form['link']
        result = subprocess.check_output(['/home/chrisg/steemit/add-link.sh', blog, link])        
        
    return list_articles(blog)




def list_articles(blog="makerhacks"):

    contents = """
        Add a link: <br/>
        <form method="post">
            <input type="text" name="link" size="35"><input type="submit" value="Add link">

        </form>


    """

    contents += "<p/>Template<br/><textarea cols=80 rows=40>![best-of-steemit.png](https://steemitimages.com/DQmR95XitKkgxh4fGukqgeaP1fSd22rhZWU5FF4xpkmEgWf/best-of-steemit.png)\n\n# Best of Steemit Roundup for " + datetime.datetime.now().strftime("%A") + " " + datetime.datetime.now().strftime("%d") + " " + datetime.datetime.now().strftime("%B") + " " + datetime.datetime.now().strftime("%Y")  + "</h1>" + postfooter + "</textarea>"
    contents += "<p>Articles<br/><textarea cols=80 rows=40>"

    # get db connection
    conn = create_connection("../articles-sqlite.db")
    contents += get_articles(conn,blog)
    contents += "</textarea>"

    return contents

# specify category
@app.route('/cat/<category>/')
def docategory(category):

    return grabcontent( category )

# specify category AND sorting
@app.route('/cat/<category>/<sorting>/')
def docategoryandsort(category,sorting):

    return grabcontent( category,sorting )

# path
@app.route('/user/<username>')
def get_user(username):

    output = username + ' has ' + s.get_account(username)['sbd_balance'] 

    return output


def grabcontent( category = "Technology", sorting ="trending" ):



    styles = "body { width: 100%; text-align: center; }"
    html = "<html><head><title>Curate!</title>"
    html += "<script src=\"https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js\"></script>"
    html += "<style>" + styles + "</style></head><body><div id='contents'  style='width: 600px; text-align: left; margin: 0px auto; '>"
    posts = s.get_posts(limit=100, sort=sorting, category=category.title(), start=None) 
    counter = 0

    #["trending", "created", "active", "cashout", "payout", "votes", "children", "hot"]:

    html+= "<a href=\"/cat/technology/\">tech</a> | <a href=\"/cat/business/\">biz</a> | <a href=\"/cat/blogging/\">blogging</a> | <a href=\"/cat/funny/\">funny</a> | <a href=\"/cat/printing3d/\">3d</a> | <a href=\"/cat/python/\">python</a><p/> " 
    html+= "<p><a href=\"/cat/cryptocurrency/\">crypto</a> | <a href=\"/cat/blog/\">blog</a> | <a href=\"/cat/bitcoin/\">btc</a> | <a href=\"/cat/money/\">$</a> | <a href=\"/cat/news/\">news</a> | <a href=\"/cat/science/\">sci</a> | <a href=\"/cat/howto/\">how</a><p/> " 
    html+= "<p><a href=\"/cat/arduino/\">Arduino</a> | <a href=\"/cat/raspberrypi/\">Pi</a> | <a href=\"/cat/making/\">Making</a> |<a href=\"/cat/printing3d/\">3DP</a> | <a href=\"/cat/design3d/\">3DD</a>" 
    html+= "<p/><textarea cols=80 rows=40>![best-of-steemit.png](https://steemitimages.com/DQmR95XitKkgxh4fGukqgeaP1fSd22rhZWU5FF4xpkmEgWf/best-of-steemit.png)\n\n# Best of Steemit Roundup for " + datetime.datetime.now().strftime("%A") + " " + datetime.datetime.now().strftime("%d") + " " + datetime.datetime.now().strftime("%B") + " " + datetime.datetime.now().strftime("%Y")  + "</h1>" + postfooter + "</textarea>"

#
#<div class="pull-left"></div>
#<blockquote></blockquote>
# <br  style="clear: both;" /><br  style="clear: both;" />
# ### [Read More]()
#<p  style="clear: both;">&nbsp;</p><p  style="clear: both;">&nbsp;</p>
#<hr>

    for post in posts:
        counter+=1
        html+= "<div id='" + str( counter ) + "' style='overflow:hidden;font-size:14pt;font-family: Source Sans Pro'>"
        html+= "</strong></em></bold></i>"
        html+= "<h1 onclick='$(\"#" + str( counter ) + " span:first\").toggle();'>"
        html+= post.title + " by " + post.author  
        html+= "</h1><span style='display:none'>"
        html+= post.body.replace( "\n", "<p>" ) 
        html+= "</span><span><form><textarea cols=80 rows=30>https://steemit.com" + post.url + "</textarea></form></span>" 
        html+= "</div><hr>"

    return md.convert(html)

