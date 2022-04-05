import argparse
import re

def exceptions(word):
    if not word:
        raise Exception('Must provide a word')

    if not (word == word.lower()):
        raise Exception('Must provide words in lower case')

def all_tweets():
    prefixes = ('#', '@', 'http', '.', 'rt')
    all_tweets = []
    for tweet in open('tweets.txt','r').readlines():
        _, _, text = tweet.partition(', ')
        text = text.replace('RT', '')
        words = text.strip().split()
        words = [word for word in words if not word.startswith(prefixes)]
        words = [re.sub(r'\W+', '', word).lower() for word in words]
        en_words = [word for word in words if any(ord(c) <= 122 for c in word)]
        tweet_text = " ".join(word for word in en_words)
        all_tweets.append(tweet_text)
    return all_tweets

def count_p(input, tweets_list):
    count = 0
    for tweet in tweets_list:
        search = re.search(r'\b' + input + r'\b', tweet)
        if search:
            count += 1
    return count

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--word', type=str)
    args = parser.parse_args()
    exceptions(args.word)
    tweets_list = all_tweets()
    countnum = count_p(args.word, tweets_list)
    print(f"The phrase '{args.word}' occurs {countnum} time(s)")

if __name__ == "__main__":
    main()
