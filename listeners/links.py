import re

import requests
from py2neo import Graph

import constants

graph = Graph(constants.neo_url)

pat = re.compile(r'(?i)\b((?:https?://|www\d{0,3}[]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?\xab\xbb\u201c\u201d\u2018\u2019]))')
r = re.compile(pat)

def onMessage(message):

	# detect url
	m = r.match(message['text'])
	if r.match is None:
		return

	url = r.group()
	url_statement = """
	MATCH (u:User {id: {u_id}})

	MATCH (m:Message {id: {m_id}})

	MERGE (u:URL {id: {url} })
	MERGE (m)-[r:HAS_URL]->(u)
	"""

	graph.cypher.execute(url_statement, {
		'u_id': message['sender_id'],
		'm_id': message['id'],
		'url': url
	})

	rsp = requests.post("http://toomba.mybluemix.net/cypher/roombamatize", json={
		'nodeType': "Message",
		'nodeId': message['id'],
		'content': url,
		'contentType': 'url'
	})

	transactions = rsp.json()
	for tx in transactions:
		graph.cypher.execute(tx)
