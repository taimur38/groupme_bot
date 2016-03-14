import logging

import requests
from py2neo import Graph

import constants

logging.basicConfig(filename="debug.log", level=logging.INFO)
graph = Graph(constants.neo_url)


def onMessage(message):
    user_statement = """
    MERGE (u:User {id: {u_id} })
    SET u.name = {name}, u.avatar_url = {avatar_url}

    CREATE (m:Message {id: {m_id} })
    SET m.date = {m_date}, m.text = {m_text}

    MERGE (u)-[r:SENT]->(m)
    """

    print(str(message))

    graph.cypher.execute(user_statement, {
        'u_id': message['sender_id'],
        'name': message['name'],
        'avatar_url': message['avatar_url'],
        'm_id': message['id'],
        'm_date': message['created_at'],
        'm_text': message['text']
    })

    rsp = requests.post("http://toomba.mybluemix.net/cypher/roombamatize", json={
        'nodeType': 'Message',
        'nodeId': message['id'],
        'content': message['text']
    })

    transactions = rsp.json()['transactions']

    for tx in transactions:
        graph.cypher.execute(tx)
