import feedparser, logging, re, time, read_url
from textblob import TextBlob
from gensim.summarization import summarize
from time import sleep
# logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)



def getItemTitles(feed):
	feed_items = feed["items"]
	titles = []
	for item in feed_items: 
		titles.append(item["title"])
	return titles

def getItemDescriptions(feed):
	feed_items = feed["items"]
	descriptions = []
	for item in feed_items: 
		descriptions.append(item["summary"])
	return descriptions

def getItemURLs(feed): 
	feed_items = feed["items"]
	urls = []
	for item in feed_items: 
		urls.append(item["link"])
	return urls

def getAvgPolarity(blb): 
	count = 0.0
	total_polarity = 0.0
	for sentence in blb.sentences: 
		count += 1
		total_polarity += sentence.sentiment.polarity
	return total_polarity/count


bbc_world_url = "http://feeds.bbci.co.uk/news/rss.xml"
cnn_world_url = "http://rss.cnn.com/rss/cnn_world.rss"
bbc_world_feed = feedparser.parse(bbc_world_url)
cnn_world_feed = feedparser.parse(cnn_world_url)


bbc_world_title_list = getItemTitles(bbc_world_feed)
bbc_world_description_list = getItemDescriptions(bbc_world_feed)
bbc_world_url_list = getItemURLs(bbc_world_feed)

cnn_world_title_list = getItemTitles(cnn_world_feed)
cnn_world_description_list = getItemDescriptions(cnn_world_feed)
cnn_world_url_list = getItemURLs(cnn_world_feed)
# for tl in title_list: 
#	print tl
# for dl in description_list: 
#	print dl

def getBlob(lst): 
	tl = [title+"\n" for title in cnn_world_title_list]
	cnn_world_blob_str = '\n'.join(tl)
	cnn_world_blob = TextBlob(cnn_world_blob_str)


# print("Average polarity for CNN: "+str(getAvgPolarity(cnn_world_blob))+"\n")

def printSummaries(titles, urls):
	big_list = zip(titles, urls)
	for ls in big_list: 
		url_stuff = read_url.getURLstuff(ls[1])
		url_stuff_sub = re.sub("By continuing to use this site, you are agreeing to the new Privacy Policy and Terms of Service.\n","",url_stuff)
		sleep(2)
		try: 
			print "\n\n\n"+ls[0]+"\n"+ls[1]+"\n"
			print summarize(url_stuff_sub, 0.07)
		except: 
			print "\nnot enough sentences..."


printSummaries(cnn_world_title_list, cnn_world_url_list)


# print cnn_world_title_list[1]
# print cnn_world_description_list[1].split("<")[0]
oneline = cnn_world_description_list[1].split("<")[0]
# print cnn_world_url_list[1]


# for sentence in blob.sentences: 
	# print(str(sentence)+"\t"+str(sentence.sentiment)+"\n")
	# print(str(sentence)+"\t"+str(sentence.sentiment.polarity)+"\n\n")



