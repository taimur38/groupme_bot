import random

import constants
from helpers import post_message


def onMessage(message):
    if 'juanita' not in message['text']:
        return

    person = random.choice(constants.people)
    adj = random.choice(constants.adjectives)

    if person == 'Taimur':
        post_message("Master Shah, I'm afraid chance has called upon thee to perform this duty")
    else:
        post_message('make that {adj} {person} do it'.format(adj=adj, person=person))
