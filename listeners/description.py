import requests

import constants
from helpers import post_message

url = "https://api.projectoxford.ai/emotion/v1.0/analyze?visualFeatures=Description"


def onMessage(message):

    if 'png' not in message['text'] and 'jpg' not in message['text']:
        return

    rsp = requests.post(url, json={'url': message['text']}, headers={'Ocp-Apim-Subscription-Key': constants.img_desc_key})

    print(rsp.text)
    if rsp.status_code != 200:
        return

    parsed = rsp.json()

    if 'descriptions' not in parsed:
        return

    if 'captions' not in parsed['descriptions']:
        return

    captions = parsed['descriptions']['captions']
    if len(captions) == 0:
        return

    description = ""
    max_score = 0

    for caption in captions:
        if caption['confidence'] > max_score:
            max_score = caption
            description = caption['text']

    post_message(description + '. I am %.2f percent confident ' % max_score * 100)
