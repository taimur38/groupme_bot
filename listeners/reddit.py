import requests

from helpers import post_message


session = requests.session()
session.headers.update({'User-Agent': '/u/taimur38'})


def onMessage(message):

    if 'http' not in message['text']:
        return

    rsp = session.get('http://www.reddit.com/search.json?q=url:' + message['text'])

    if rsp.status_code != 200:
        return

    parsed = rsp.json()

    if len(parsed['data']['children']) == 0:
        return

    post_message(get_top_comment(parsed['data']['children'][0]['data']['permalink']))


def get_top_comment(permalink):

    if '?' in permalink:
        permalink = permalink.split('?')[0]

    rsp = session.get('http://reddit.com' + permalink + '.json')

    if rsp.status_code != 200:
        return

    parsed = rsp.json()

    if len(parsed) < 2:
        return

    return parsed[1]['data']['children'][0]['data']['body']
