from time import sleep
import logging

from flask import Flask, request

import constants
from py2neo import Graph
from listeners import listeners
from helpers import post_message

app = Flask(__name__)
urls = []

logging.basicConfig(filename="debug.log", level=logging.INFO)

graph = Graph(constants.neo_url)

@app.route('/groupme', methods=['POST'])
def message():
    parsed = request.get_json()

    message = parsed['text'].lower().strip()
    print(message)

    sleep(.5)

    for listener in listeners:
        try:
            listener(parsed)
        except:
            logging.exception('error')

    return 'ok'


@app.route('/send/<msg>')
def say(msg):
    post_message(msg)
    return 'sent ' + msg


@app.route('/links')
def get_links():
    link_statement = """
    MATCH (u:User)--(m:Message)--(l:Link)
    return u.name as name, m.date as date, l.id as link
    order by toint(date) desc
    limit 15
    """

    rsp = graph.cypher.execute(link_statement)

    template = """
    <div><a href="{link}">{user} submitted on {date}</a></div>
    """

    divs = ""
    for r in rsp:
		datestring = datetime.fromtimestamp(int(r['date'])).strftime('%m/%d %H:%M:%S')
        divs += template.format(link=r['link'], user=r['name'], date=datestring)

    return """
    <html>
    <body>
    {divs}
    </body>
    </html>""".format(divs=divs)


@app.route("/")
def status():
    return 'hello'

app.run(host='0.0.0.0', debug=True)
