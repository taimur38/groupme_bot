import requests

from helpers import post_message


session = requests.session()
session.headers.update({'User-Agent': '/u/taimur38'})


def onMessage(message):

    if 'http' not in message['text']:
        return

    rsp = session.get('http://www.reddit.com/.json')

    print(rsp.text)
    if rsp.status_code != 200:
        return

    parsed = rsp.json()

    for child in parsed['data']['children']:
        if message['text'] in child['data'].get('url', ''):
            post_message(get_top_comment(child['data']['permalink']))
            return


def get_top_comment(permalink):

    rsp = session.get('http://reddit.com' + permalink + '.json')

    print(rsp.text)
    if rsp.status_code != 200:
        return

    parsed = rsp.json()

    if len(parsed) < 2:
        return

    return parsed[1]['data']['children'][0]['data']['body']
