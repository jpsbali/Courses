import json
import sys

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

 		for tweet in tweets:
 			try:
 				tweetText = tweet['text']
 				print countTweetSentimentScore(sentimentDict, tweetText)
			except Exception, e:
 				pass

if __name__ == '__main__':
    main()
