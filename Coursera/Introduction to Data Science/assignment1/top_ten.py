import json, sys


def main():
	tweetFile = open(sys.argv[1])
	tweets = [json.loads(tweet) for tweet in tweetFile.readlines()]
	tweetFile.close()

	#defines
	hashtags = []
	uniqueHashtags = {}
	toptenHashtags = []

	#Read in entities->hashtag->text
	for tweet in tweets:
		try:
			if tweet.has_key("entities") and tweet["entities"]["hashtags"] != []:
				for hashtag in tweet["entities"]["hashtags"]:
					if hashtag["text"].isalnum():
						hashtags.append((hashtag["text"]))
		except Exception, e:
			pass
			
	#Find Unique Hashtags
	for hashtag in hashtags:
		if hashtag in uniqueHashtags:
			uniqueHashtags[hashtag] += 1
		else:
			uniqueHashtags[hashtag] = 1		

	#Sort Hashtags and print top ten
	for hashtag in sorted(uniqueHashtags, key=uniqueHashtags.get, reverse=True):
		toptenHashtags.append((hashtag, uniqueHashtags[hashtag]))
	toptenHashtags = toptenHashtags[0:10]	
	for (x,y) in toptenHashtags:
		print x + " " + str(y/1.0)


if __name__ == '__main__':
    main()
