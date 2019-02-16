import feedparser, time, sys, threading
from textblob import TextBlob
from subprocess import check_output
from time import sleep


bbc_world_url = "http://feeds.bbci.co.uk/news/rss.xml"

db = '/home/alexander/Desktop/NLP_final/feeds.db'

getCurrentTimeMillis = lambda: int(round(time.time() * 1000)) # may not want int for shorter refresh times? 
current_timestamp = getCurrentTimeMillis()
print current_timestamp
# limit = 12 * 1000 * 3600
limit = 1000 * 3600


# Get the feed data. 
bbc_world_feed = feedparser.parse(bbc_world_url)

posts_to_print = []
posts_to_skip = []
for entry in bbc_world_feed.entries: 
	print entry
for entry in bbc_world_feed.entries: 
	headline = entry.title
	with open(db, 'r') as database: 
		for line in database:  
			if headline in line.decode('utf-8'):
				full_entry = line.split('|', 1)
				ts = long(full_entry[1])
				if current_timestamp - ts > limit:
					posts_to_skip.append(line)
				else: 
					posts_to_print.append(line)

#print posts_to_print
#print posts_to_skip

f = open(db, "r")
lines = f.readlines()
f.close()
f = open(db, "w")
f.write(str(current_timestamp)+"\n\n")
for post in posts_to_print: 
	f.write(line)
f.close()



	
