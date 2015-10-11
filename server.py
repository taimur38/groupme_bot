from time import sleep
import re
import logging

from flask import Flask, request

from listeners import listeners

app = Flask(__name__)
urls = []

pat = re.compile(r'(?i)\b((?:https?://|www\d{0,3}[]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?\xab\xbb\u201c\u201d\u2018\u2019]))')
r = re.compile(pat)

logging.basicConfig(filename="debug.log", level=logging.INFO)

@app.route('/groupme', methods=['POST'])
def message():
    parsed = request.get_json()

    message = parsed['text'].lower().strip()
    print(message)

    sleep(.5)

    print(str(listeners))
    for listener in listeners:
        try:
            listener(parsed)
        except:
            logging.exception('error')

    return 'ok'


@app.route('/links')
def debug():

    output = "<h1>Links</h1><ul>{links}</ul>"

    links = ""
    for u in urls:
        links += "<li><a href={link} target='_blank'>{text}</a></li>".format(link=u, text=u)

    return output.format(links=links)


@app.route("/")
def status():
    return 'hello'

app.run(host='0.0.0.0', debug=True)
