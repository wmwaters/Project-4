#Project 4
#William Waters
#SI 206 Fall 2017

import json
import sqlite3
import requests
import datetime as dt

import facebook_info #get personal access token file
access_token = facebook_info.access_token #getting facebook access token from file in directory

import plotly
plotly.tools.set_credentials_file(username = 'wmwaters', api_key = 'ekYBCvTD8xMpGdM8p49r') #setting api access code for ploy.ly
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
try: #opening cache file if it exists
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    cache_file.close()
    CACHE = json.loads(cache_contents)
except: #creating cache file from pulled data if there isn't already a cache
	api_url = "https://graph.facebook.com/v2.11/me/"
	url_parameters = {} #building url to get 1000 posts from Facebook
	url_parameters["access_token"] = access_token
	url_parameters["fields"] = "posts.limit(1000)"
	page = requests.get(api_url, url_parameters) #requested Facebook data
	CACHEpre = page.json()
	CACHE = {"posts" : []} #got only 73 back when pulling 100 posts, so this following loop limits from 1000 items to 100 posts
	i = 0
	while (len(CACHE["posts"]) < 100):
		CACHE["posts"].append(CACHEpre['posts']['data'][i])
		i += 1
	cache_file = open(CACHE_FNAME, 'w')
	json.dump(CACHE, cache_file)
	cache_file.close()

conn = sqlite3.connect('project4.sqlite') #creating or opening database
cur = conn.cursor()
cur.execute('DROP TABLE IF EXISTS Posts') #deleting table if it already exists
cur.execute("CREATE TABLE Posts (id TEXT PRIMARY KEY, posttime TEXT)") #setting items in database
weekdic = {}
for post in CACHE['posts']: #creating datetime object for each post
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
	weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
	if weekdays[daytimeobj.weekday()] in weekdic: #counting the number of posts on each day
		weekdic[weekdays[daytimeobj.weekday()]] += 1
	else:
		weekdic[weekdays[daytimeobj.weekday()]] = 1

	tp = (post["id"], daytimeobj) #creating tuple to insert into database
	cur.execute("INSERT INTO Posts (id, posttime) VALUES (?,?)", tp) #putting item into database


conn.commit()
conn.close()

day_values = [] #creating x-axis values list
day_values.append(weekdic["Monday"])
day_values.append(weekdic["Tuesday"])
day_values.append(weekdic["Wednesday"])
day_values.append(weekdic["Thursday"])
day_values.append(weekdic["Friday"])
day_values.append(weekdic["Saturday"])
day_values.append(weekdic["Sunday"])
#creating x-y data for plotly as trace0
trace0 = go.Bar(x = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], y = day_values, name = 'Name of Trace 0')
data = [trace0] #turning trace0 into a list
#making the graph have a title and axis labels
layout = go.Layout(title = 'Facebook Posts By Day of Week', xaxis = dict(title = 'Days of Week', titlefont = dict(family = 'Courier New, monospace', size = 18, color = '#7f7f7f')), yaxis = dict(title = 'Number of Facebook Posts', titlefont = dict(family = 'Courier New, monospace', size = 18, color = '#7f7f7f')))
#creating a figure from the combined data and layout objects
fig = go.Figure(data = data, layout = layout)
#sending my graph to plot.ly
py.plot(fig, filename = '206 Final Project Facebook Post Graph')