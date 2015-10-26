from time import sleep
import logging

from flask import Flask, request

from listeners import listeners
from helpers import post_message

app = Flask(__name__)
urls = []

logging.basicConfig(filename="debug.log", level=logging.INFO)


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


@app.route("/")
def status():
    return 'hello'

app.run(host='0.0.0.0', debug=True)
