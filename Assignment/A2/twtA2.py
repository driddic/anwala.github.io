'''
	prerequisites:
	0. create a twitter account
	1. obtain your access tokens: https://apps.twitter.com/
		1.0 create new app
	2. install tweepy (pip install tweepy)

	credit:
	http://docs.tweepy.org/en/v3.4.0/streaming_how_to.html
	http://adilmoujahid.com/posts/2014/07/twitter-analytics/
	https://pythonprogramming.net/twitter-api-streaming-tweets-python-tutorial/

	Tweet JSON:, use http://jsonviewer.stack.hu/ to view object
	https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/intro-to-tweet-json

	rate limiting:
	https://developer.twitter.com/en/docs/basics/rate-limiting

	streaming rate limiting:
	https://developer.twitter.com/en/docs/tweets/filter-realtime/guides/connecting.html
'''

#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import time
import re


#get keys from: https://apps.twitter.com/
#consumer key, consumer secret, access token, access secret.
ckey = 'lTXqzqSptLXqggl6mo7iCeYR2'
csecret = '4aNO3iMo6ZtpuHt3Ssj7EA5bKdZ6SVuHxQO2vamjksC0v2lRVl'
atoken = '170079373-9R0y6xZPIwHXpnJoWzytGpcwLvSUPY5GijrZC4TL'
asecret = 'qRjsuf8lKMOgwcU9YSa5ItIu1XCFAq4uz99Oc4ZA6DquA'

class listener(StreamListener):

	def on_data(self, data):
		tweet = data.split(',"text":"')[1].split('","source:')[0]
		print(tweet)
		saveTime = str(time.time())+'::'+tweet
		saveTofile=open('a2try1.json','a')
		saveTofile.write(data)
		saveTofile.write('\n')
		saveTofile.close()
		return True



	def on_error(self, status):
		print( status )
		if status_code == 420:
				#returning False in on_data disconnects the stream
					return False

		return True

	def on_data(self, data):
		#learn about tweet json structure: https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/intro-to-tweet-json
		tweetJson = json.loads(data)

		#tweet = tweetJson['text']
		username = tweetJson['user']['screen_name']
		links = tweetJson['entities']['urls']

		if( len(links) != 0 and tweetJson['truncated'] == False ):
			links = self.getLinksFromTweet(links)

			print( username )
			for l in links:
				print('\t', l)
			print ()


		#print('...sleep for 5 seconds')
		time.sleep(5)

		return True


	def getLinksFromTweet(self, linksDict):

		links = []
		url = '<p>Hello World</p><a href="http://example.com">More Examples</a><a href="http://example2.com">Even More Examples</a>'

		urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', url)


		for uri in linksDict:
			links.append( uri['expanded_url'] )

		return links

#handles Twitter authetification and the connection to twitter API

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

twitterStream = Stream(auth, listener())
twitterStream.filter(track=["rockets"])
