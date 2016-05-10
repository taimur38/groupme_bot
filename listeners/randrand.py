from random import randint
from helpers import post_message


def onMessage(message):
    if 'juanita roll' not in message['text'].lower():
        return

    splits = message['text'].split(" ")
    if len(splits) > 2:
        top = int(splits[2])
        post_message(str(randint(0, top)))
    else:
        post_message(str(randint(0, 10)))
