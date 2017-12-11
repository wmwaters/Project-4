#Project 4
#William Waters
#SI 206 Fall 2017

import json
import sqlite3
import requests
import facebook_info #get personal access token
access_token = facebook_info.access_token
import datetime

import sys #prevent unicode errors
def uprint(*objects, sep=' ', end='\n', file=sys.stdout):
    enc = file.encoding
    if enc == 'UTF-8':
        print(*objects, sep=sep, end=end, file=file)
    else:
        f = lambda obj: str(obj).encode(enc, errors='backslashreplace').decode(enc)
        print(*map(f, objects), sep=sep, end=end, file=file)

CACHE_FNAME = "206_Project4_cache.json"
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    cache_file.close()
    CACHE = json.loads(cache_contents)
except:
	api_url = "https://graph.facebook.com/v2.11/me/"
	url_parameters = {}
	url_parameters["access_token"] = access_token
	url_parameters["fields"] = "posts.limit(100)"
	page = requests.get(api_url, url_parameters)
	CACHE = page.json()
	cache_file = open(CACHE_FNAME, 'w')
	json.dump(CACHE, cache_file)
	cache_file.close()

conn = sqlite3.connect('project4.sqlite')
cur = conn.cursor()
cur.execute('DROP TABLE IF EXISTS Posts')
cur.execute("CREATE TABLE Posts (id TEXT PRIMARY KEY, posttime TEXT)")
for post in CACHE['posts']['data']:
	uprint(post)