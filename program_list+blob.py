from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import RegexpTokenizer
stemmer = SnowballStemmer("english")
tokenizer = RegexpTokenizer(r'\w+')
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
    pos_list = prepare_word_lists(pos)
    neg_list = prepare_word_lists(neg)
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

            tweet = stemmer.stem(tweet)
            tweet = tokenizer.tokenize(tweet)
            tweet_set = set(tweet)

            # Textblob. sentiment is a float. ranging from -1(negative) to 1(positive)

            case = TextBlob(original_tweet)
            sentiment = case.sentiment.polarity
            prediction = ''

            positive_words = tweet_set.intersection(pos_list)
            negative_words = tweet_set.intersection(neg_list)

            if len(positive_words) > len(negative_words):
                prediction = '4'

            elif len(positive_words) < len(negative_words):
                prediction = '0'

            if sentiment < 0:
                prediction = '0'


            score = 0
            if actual_sentiment == prediction:
                score = 1
                totalscore = totalscore +1

        #calculated percentage over a dataset of 50.000 tweets
        percentage = totalscore / 50000 * 100
        print('total score: {}, accuracy: {}'.format(totalscore, round(percentage,1)))
        # print the time it took to compute
        print('total runtime: {}'.format(time.clock() - start_time))

if __name__ == "__main__":
    main()