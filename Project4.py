#Project 4
#William Waters
#SI 206 Fall 2017

import json
import sqlite3
import requests
import facebook_info #get personal access token
access_token = facebook_info.access_token
import datetime as dt
import plotly
plotly.tools.set_credentials_file(username='wmwaters', api_key='ekYBCvTD8xMpGdM8p49r')
import plotly.plotly as py
import plotly.graph_objs as go




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
	url_parameters["fields"] = "posts.limit(1000)"
	page = requests.get(api_url, url_parameters)
	CACHEpre = page.json()
	CACHE = {"posts" : []}
	i = 0
	while (len(CACHE["posts"]) < 100):
		CACHE["posts"].append(CACHEpre['posts']['data'][i])
		i += 1
	cache_file = open(CACHE_FNAME, 'w')
	json.dump(CACHE, cache_file)
	cache_file.close()

conn = sqlite3.connect('project4.sqlite')
cur = conn.cursor()
cur.execute('DROP TABLE IF EXISTS Posts')
cur.execute("CREATE TABLE Posts (id TEXT PRIMARY KEY, posttime TEXT)")
weekdic = {}
for post in CACHE['posts']:
	split = post["created_time"].split('T')
	day = split[0].split('-')
	time = split[1].split(':')
	time2 = time[2].split('+')
	year = int(day[0])
	month = int(day[1])
	day = int(day[2])
	hour = int(time[0])
	minute = int(time[1])
	second = int(time2[0])
	daytimeobj = dt.datetime(year, month, day, hour, minute, second)
	weekda = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
	if weekda[daytimeobj.weekday()] in weekdic:
		weekdic[weekda[daytimeobj.weekday()]]+=1
	else:
		weekdic[weekda[daytimeobj.weekday()]]=1

	tp = (post["id"], daytimeobj)
	cur.execute("INSERT INTO Posts (id, posttime) VALUES (?,?)", tp)


conn.commit()
conn.close()
day_values = []
day_values.append(weekdic["Monday"])
day_values.append(weekdic["Tuesday"])
day_values.append(weekdic["Wednesday"])
day_values.append(weekdic["Thursday"])
day_values.append(weekdic["Friday"])
day_values.append(weekdic["Saturday"])
day_values.append(weekdic["Sunday"])
print(day_values)
data = [go.Bar(
            x=['giraffes', 'orangutans', 'monkeys'],
            y=[20, 14, 23])]
#data = [go.Bar(x = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], y = day_values)]
py.plot(data, filename='basic-bar')