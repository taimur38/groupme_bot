import re
from datetime import datetime, timedelta

import requests
from py2neo import Graph

import constants
from helpers import post_message

graph = Graph(constants.neo_url)

# pat = re.compile(r'(?i)\b((?:https?://|www\d{0,3}[]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?\xab\xbb\u201c\u201d\u2018\u2019]))')
pat = re.compile(r'(https?.\/\/+)([^ ]+)')
r = re.compile(pat)

def onMessage(message):

	m = r.search(message['text'])
	if m is None:
		return

	url = m.group()
	print(url)

	# check if it exists

	check_statement = """
	MATCH (u:User)--(m:Message)--(l:Link {id: {url}})
	return u.name as name, m.date as date
	"""

	previous_cases = graph.cypher.execute(check_statement, {
		'url': url
	})

	for pc in previous_cases:
		datestring = (datetime.fromtimestamp(int(pc['date'])) - delta).strftime('%m/%d %H:%M:%S')
		name = pc['name'].split(' ')[-1]

		post_message("Mr. {user} posted that on {ds}".format(user=name, ds=datestring))


	url_statement = """
	MATCH (m:Message {id: {m_id}})

	MERGE (l:Link {id: {url} })
	MERGE (m)-[r:HAS_LINK]->(l)
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

	transactions = rsp.json()['transactions']
	for tx in transactions:
		graph.cypher.execute(tx)
