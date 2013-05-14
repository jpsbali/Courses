import json,sys


def countTweetSentimentScore(sentimentDict, tweetText):
		tweetWords = tweetText.encode('utf8').split()
		tweetSentiment = 0
		for tweetWord in tweetWords:
			if tweetWord in sentimentDict:
				tweetSentiment += sentimentDict[tweetWord]
		return tweetSentiment


def main():
		sentimentsFile = open(sys.argv[1])
		tweetFile = open(sys.argv[2])

		sentiments = [sentimentsLine.split('\t') for sentimentsLine in sentimentsFile.readlines()]
		sentimentDict = { k: int(v) for (k, v) in sentiments }

		tweets = [json.loads(tweet) for tweet in tweetFile.readlines()]

		sentimentsFile.close()
		tweetFile.close()

		tweetSentimentDictionary = {}

 		for tweet in tweets:
 			try:
				#junkChars = dict.fromkeys(map(ord, ':;,.!?'), None)
 				#tweetText = tweet['text'].translate(junkChars).lower()
 				tweetText = tweet['text']
 				tweetSentiment = countTweetSentimentScore(sentimentDict, tweetText)
				#print tweetText.encode('utf8')
				#print tweetSentiment

				tweetWords = tweetText.split()

				for tweetWord in tweetWords:
					if tweetWord in tweetSentimentDictionary:
						tweetSentimentDictionary[tweetWord]['sentiment'] += tweetSentiment
						tweetSentimentDictionary[tweetWord]['count'] += 1
					else:
						tweetSentimentDictionary[tweetWord] = {'sentiment': tweetSentiment,'count': 1}
			except Exception, e:
				pass
 
		for k, v in tweetSentimentDictionary.items():
			if is_ascii(k):
				print k, float(v['sentiment'])/v['count']


def is_ascii(s):
	return all(ord(c) < 128 for c in s)

if __name__ == '__main__':
    main()
