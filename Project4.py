#Project 4
#William Waters
#SI 206 Fall 2017

import json
import sqlite3
import requests
import facebook_info.py #get personal access token

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
    cache_file = open(CACHE_FNAME,'r')
    cache_contents = cache_file.read()
    cache_file.close()
    CACHE_DICTION = json.loads(cache_contents)
except:
    r = requests.get("https://graph.facebook.com/v2.11/me/",params={"limit":2, "access_token":access_token})


