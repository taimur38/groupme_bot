import constants
from helpers import post_message

index = 0


def onMessage(message):
    if 'juanita' not in message['text'].lower():
        return

    global index
    index = (index + 1) % len(constants.people)
    person = constants.people[index]

    if person == 'Taimur':
        post_message("Master Shah, I'm afraid chance has called upon thee to perform this duty")
    else:
        post_message('make {person} do it'.format(person=person))
