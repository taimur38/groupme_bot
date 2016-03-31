import requests

import constants
from helpers import post_message


url = "https://api.projectoxford.ai/emotion/v1.0/recognize"


def onMessage(message):

    if 'png' not in message['text'] or 'jpg' not in message['text']:
        return

    # assuming the message text is just a url.

    rsp = requests.post(url, json={"url": message['text']}, headers={'Ocp-Apim-Subscription-Key': constants.emotion_key})

    if rsp.status_code != 200:
        return

    parsed = rsp.json()

    if len(parsed) == 0:
        return

    emotions = []
    for face in parsed:
        for emotion, score in face['scores']:
            if score > .5:
                emotions.append(emotion)

    if len(emotions) == 0:
        return

    if len(emotions) > 1:
        post_message('the emotions in this picture are: ' + ', '.join(emotions[:-1]) + ' and ' + emotions[-1])
    else:
        post_message('the emotions in this picture are: ' + emotions[0])
