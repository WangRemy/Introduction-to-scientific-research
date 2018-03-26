from textblob import TextBlob
import csv
import time

neg = open('negative-words.txt', 'r')
pos = open('positive-words-with.txt', 'r')
# Stopwords from https://www.ranks.nl/stopwords
stop = open('stopwords.txt', 'r')

def prepare_word_lists(text_file):
    words_list = []
    for line in text_file:
        line = line.strip()
        line = line.lower()
        words_list.append(line)
    return words_list



def main():
	start_time = time.clock()

	totalscore = 0
	stop_list = prepare_word_lists(stop)

	# the dataset is read
	with open('totalset.csv', encoding='latin-1') as csvfile:
		csvreader = csv.reader(csvfile, delimiter = ',')
		for row in csvreader:
			actual_sentiment = row[0]
			id_ = row[1]
			original_tweet = row[5].lower()
			tweet = ''

			# stopwords are extracted from the tweets
			for token in original_tweet.split():
				if token not in stop_list:
					tweet += ' ' + token


			case = TextBlob(original_tweet)
			sentiment = case.sentiment.polarity
			prediction = ''
			# Textblob. sentiment is a float. ranging from -1(negative) to 1(positive)
			if sentiment < 0:
				prediction = '0'
			else:
				prediction = '4'

			score = 0
			if actual_sentiment == prediction:
				score = 1
				totalscore = totalscore +1

		#calculated percentage over a dataset of 50.000 tweets
		percentage = totalscore / 50000 * 100
		print('total score: {}, accuracy {}'.format(totalscore, round(percentage,1)))
		# print the time it took to compute
		print('total runtime: {}'.format(time.clock() - start_time))

if __name__ == "__main__":
    main()