import re
import requests

import constants
from helpers import post_message


pat = re.compile(r'(https?.\/\/+)([^ ]+)')
url = "https://api.projectoxford.ai/emotion/v1.0/recognize"


def onMessage(message):

    match = pat.search(message['text'])
    if not match:
        return

    url = match.group()
    if 'png' not in message['text'] and 'jpg' not in message['text']:
        return


    rsp = requests.post(url, json={"url": match}, headers={'Ocp-Apim-Subscription-Key': constants.emotion_key})

    if rsp.status_code != 200:
        return

    parsed = rsp.json()

    emotions = []
    for face in parsed:
        for emotion, score in face['scores'].items():
            if score > .5:
                emotions.append(emotion)

    if len(emotions) == 0:
        return

    if len(emotions) > 1:
        post_message('the emotions in this picture are: ' + ', '.join(emotions[:-1]) + ' and ' + emotions[-1])
    else:
        post_message('the emotions in this picture are: ' + emotions[0])
