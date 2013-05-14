import json, sys

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

		stateHappinessIndex	= {}

 		for tweet in tweets:
 			try:
 				tweetText = tweet['text']
 				tweetSentiment =  countTweetSentimentScore(sentimentDict, tweetText)

				if tweet['place']['country_code'] == 'US':
			 		town, state = tweet['place']['full_name'].split(', ')
				
				if state == 'San Francisco':
					state='CA'

				if state in stateHappinessIndex:
					stateHappinessIndex[state] += tweetSentiment
				else:
					stateHappinessIndex[state] = tweetSentiment

			except Exception, e:
 				pass
		
		#for state, happiness in stateHappinessIndex.items():
		#	print state, happiness

		stateTweetSentiment = 0.0
		happiestState = ""
		for key, value in stateHappinessIndex.iteritems():
			if value > stateTweetSentiment:
				happiestState = key
				stateTweetSentiment = value
		print happiestState

if __name__ == '__main__':
    main()
