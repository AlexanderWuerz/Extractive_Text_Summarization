import feedparser, time, sys, threading
from textblob import TextBlob
from subprocess import check_output
from time import sleep


bbc_world_url = "http://feeds.bbci.co.uk/news/rss.xml"

db = '/home/alexander/Desktop/NLP_final/feeds.db'
feed_name = "BBC WORLD NEWS"

# Set the time limit to keep feeds in the database. 
time_limit = 12 * 1000 * 3600 # 15 seconds 

getCurrentTimeMillis = lambda: int(round(time.time() * 1000)) # may not want int for shorter refresh times? 
current_timestamp = getCurrentTimeMillis()
print current_timestamp

def isInDB(headline): 
	with open(db, 'r') as database: 
		for line in database:
			if headline in line.decode('utf-8'): 
				return True 
	return False

# Returns true iff the headline is not in the database already.
def shouldIStay(headline): 
	with open(db, 'r') as database: 
		for line in database:
			if headline not in line.decode('utf-8'): 
				return True 
	return False 	

# Returns true iff the headline is in the database and the timestamp is too old. 
def shouldIGo(headline):
	global current_timestamp
	global time_limit
	with open(db, 'r') as database: 
		for line in database:  
			if headline in line.decode('utf-8'): 
				full_entry = line.split('|', 1)
				ts = long(full_entry[1])
				# if current_timestamp - ts > time_limit: 
				if current_timestamp > ts: 
					return True
	return False

# Returns a list of the entries that will be printed and 
def getListToPrint(feed): 
	posts = []
	for entry in feed.entries: 
		headline = entry.title
		if not shouldIStay(headline):
		# if not isInDB(headline): 
			posts.append(headline)
	return posts

# Returns a list of the entries that will be skipped. 
def getListToSkip(feed): 
	posts = []
	for entry in feed.entries: 
		headline = entry.title
		# if shouldIStay(headline): 
		# if isInDB(headline): 
		if shouldIGo(headline): 
			posts.append(headline)
	return posts

def updateDB(p2p): 
	global db
	fl = open(db, 'a')
	for headline in p2p: 
		if not shouldIStay(headline): 
			fl.write((headline+'|'+str(current_timestamp)+'\n').encode('utf-8'))
	fl.close()

def outputNewPosts(p2p, p2s): 
	count = 0
	blockcount = 0
	global feed_name
	for headline in p2p: 
		if count % 5 == 1:
       			print("\n" + time.strftime("%a, %b %d %I:%M %p") + '  ((( ' + feed_name + ' - ' + str(blockcount) + ' )))')
        		print("-----------------------------------------\n")
        		blockcount += 1
    		print(headline + "\n")
    		count += 1

def outputInit(feed): 
	# Get the posts to print and the posts to skip.  
	posts_to_print = getListToPrint(feed)
	posts_to_skip = getListToSkip(feed)

	# Update the database. 
	updateDB(posts_to_print, posts_to_skip)

	
	for headline in posts_to_print: 
    		print(headline + "\n")

def outputSleep(): 
	global bbc_world_url
	feed = feedparser.parse(bbc_world_url)
	# Get the posts to print and the posts to skip.  
	posts_to_print = getListToPrint(feed)
	posts_to_skip = getListToSkip(feed)

	# Update the database. 
	updateDB(posts_to_print, posts_to_skip)

	
	for headline in posts_to_print: 
    		print(headline + "\n")
	
	#outputSleep()



# Get the feed data. 
bbc_world_feed = feedparser.parse(bbc_world_url)

# outputInit(bbc_world_feed)
# outputSleep()
posts_to_print = getListToPrint(bbc_world_feed)
posts_to_skip = getListToSkip(bbc_world_feed)
updateDB(posts_to_print)

print posts_to_skip
print posts_to_print

print current_timestamp
# Output the new posts. 
# outputNewPosts(posts_to_print, posts_to_skip)







