import requests
import constants

def post_message(text):
    rsp = requests.post(constants.groupme_endpoint, json={
        'text': text,
        'bot_id': constants.groupme_id
    })

    return rsp.status_code == 200
