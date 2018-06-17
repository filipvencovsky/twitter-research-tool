# search_twitter.py
# modified from script developed by Jukka Huhtamaki
# available from https://github.com/jukkahuhtamaki/demo-twitter-collector
import simplejson as json

with open('keychain.json') as f:
  keychain = json.load(f)

print keychain.keys()

from requests_oauthlib import OAuth1

def get_oauth():
  oauth = OAuth1(keychain['CONSUMER_KEY'],
              client_secret=keychain['CONSUMER_SECRET'],
              resource_owner_key=keychain['OAUTH_TOKEN'],
              resource_owner_secret=keychain['OAUTH_TOKEN_SECRET'])
  return oauth

oauth = get_oauth()

import requests

# In this example tweets are extracted about #OECDForum
url = 'https://api.twitter.com/1.1/search/tweets.json?q=oecdforum&&count=1000'
# To search data on something else replace the "oecdforum" with your search string

r = requests.get(url=url, auth=get_oauth())
print r

with open('sample.json','w') as f:
  json.dump(r.json(),f,indent=1)

import networkx as nx

network = nx.DiGraph()
for status in r.json()['statuses']:
  # print status['text']
  # print status['entities']['user_mentions']
  for mentioned in status['entities']['user_mentions']:
    print status['user']['screen_name'], mentioned['screen_name']
    if not network.has_edge(status['user']['screen_name'],
      mentioned['screen_name']):
      network.add_edge(status['user']['screen_name'],
        mentioned['screen_name'], weight=0)
    network[status['user']['screen_name']][mentioned['screen_name']]['weight'] += 1

nx.readwrite.gexf.write_gexf(network,'network.gexf')