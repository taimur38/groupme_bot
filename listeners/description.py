import requests

import constants
from helpers import post_message

url = "https://api.projectoxford.ai/vision/v1.0/analyze?visualFeatures=Description"


def onMessage(message):

    if 'png' not in message['text'] and 'jpg' not in message['text']:
        return

    rsp = requests.post(url, json={'url': message['text']}, headers={'Ocp-Apim-Subscription-Key': constants.img_desc_key})

    print(rsp.text)
    if rsp.status_code != 200:
        return

    parsed = rsp.json()

    if 'description' not in parsed:
        return

    if 'captions' not in parsed['description']:
        return

    captions = parsed['description']['captions']
    if len(captions) == 0:
        return

    description = ""
    max_score = 0

    for caption in captions:
        print(caption)
        if caption['confidence'] > max_score:
            max_score = caption['confidence']
            description = caption['text']

    post_message(description)
