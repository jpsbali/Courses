import json,sys

def is_ascii(s):
	return all(ord(c) < 128 for c in s)

def main():
	tweetFile = open(sys.argv[1])
	tweets = [json.loads(tweet) for tweet in tweetFile.readlines()]
	tweetFile.close()
 
	wordFrequency = {}
	for tweet in tweets:
		try:
			tweetText = tweet['text']
			tweetWords = tweetText.split()
			for tweetWord in tweetWords:
				if tweetWord in wordFrequency:
					wordFrequency[tweetWord] += 1
				else:
					wordFrequency[tweetWord] = 1
		except Exception, e:
			pass

	totalWords = sum(v for k, v in wordFrequency.items())
	for k, v in wordFrequency.items():
		if is_ascii(k):
			print k, float(v) / totalWords
 
if __name__ == '__main__':
	main()
