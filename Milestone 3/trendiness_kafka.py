import argparse
import math
import sys
import re
import time
import signal
import psycopg

DB_USER = 'gb760'
DB_NAME = 'twitter'

EPSILON = 0.0000001

def exceptions(word):
    if not word:
        raise Exception('Must provide a word')
    if not (word == word.lower()):
        raise Exception('Must provide words in lower case')

def get_all_words(text_list):
  all_words = []
  for tweet in text_list:
    words = tweet.strip().split()
    for i in words:
      all_words.append(i)
  return all_words

def get_time():
    connection = psycopg.connect(user=DB_USER, dbname=DB_NAME)
    cursor = connection.cursor()
    query_command = "SELECT time_stamp FROM tweets ORDER BY time_stamp DESC LIMIT 1"
    cursor.execute(query_command)
    time = cursor.fetchone()[0]
    if connection:
        cursor.close()
        connection.close()
    return(time)

def get_all_tweets(t, condition):
    connection = psycopg.connect(user=DB_USER, dbname=DB_NAME)
    cursor = connection.cursor()
    if condition == 1:
        t_start = t[:-2] + '00'
    else:
        t = t.split('-')
        t[-2] = str(int(t[-2])-1) # t[-2] minute
        if len(t[-2]) < 2: # 10 min -> 09 min
            t[-2] = '0' + t[-2]
        elif t[-2] == '00': # 10h:00m -> 09h:59m
            t[-2] = '59'
            t[-3] = str(int(t[-3])-1)
            if len(t[-3]) < 2:
                t[-3] = '0' + t[-3]
        elif t[-3] == '00' and t[-2] == '00': # 00h -> 23h yesterday
            t[-3] = '23'
            t[-2] = '59'
            t[-4] = str(int(t[-4])-1)
            if (len(t[-4]) < 2) and (len(t[-4]) > 0):
                t[-4] = '0' + t[-4]
            elif t[-4] < 0:
                t[-5] = str(int(t[-5])-1)
        t[-1] = '00' # t[-1] sec
        t_start = '-'.join(t)
        t[-1] = '59'
        t = '-'.join(t)
    query_command = "SELECT content FROM tweets WHERE (time_stamp BETWEEN '" + t_start + "' AND '" + t +"') ORDER BY time_stamp DESC"
    cursor.execute(query_command)
    tweets = cursor.fetchall()

    if connection:
        cursor.close()
        connection.close()
    return(tweets)

def clean_text(text_list):
    tweets = []
    prefixes = ('#', '@', 'https')
    all_tweets = []
    for tup in text_list:
        tup =  tup[0]
        tweets.append(tup)
    for tweet in tweets:
        tweet = tweet.replace('RT', '')
        terms = tweet.strip().split()
        terms = [word for word in terms if not word.startswith(prefixes)]
        words = [re.sub(r'\W+', '', word).lower() for word in terms]
        en_words = [word for word in words if any(ord(c) <= 122 for c in word)]
        tweet_text = " ".join(word for word in en_words)
        all_tweets.append(tweet_text)
    return all_tweets

def countnum(inputs, tweets_list):
    count = 0
    for tweet in tweets_list:
        search = re.search(r'\b' + inputs + r'\b', tweet)
        if search:
            count += 1
    return count
    
def word_count(word):
    count_in_minutes = []
    for i in range(2):
        all_words = clean_text(get_all_tweets(get_time(),i))
        count_in_minutes.append(countnum(word, all_words))
    return count_in_minutes

def unique_sizes():
    unique_sizes_in_minutes = []
    for i in range(2):
        text = get_all_words(clean_text(get_all_tweets(get_time(),i)))
        size = len(set(text))
        unique_sizes_in_minutes.append(size)
    return unique_sizes_in_minutes

def all_words_sizes():
    all_sizes_in_minutes = []
    for i in range(2):
        text = get_all_words(clean_text(get_all_tweets(get_time(),i)))
        size = len(text)-text.count('')
        all_sizes_in_minutes.append(size)
    return all_sizes_in_minutes

def calc_prob(count, total_word, unique_size):
    prob = []
    for i in range(2):
        prob.append((1+count[i]) / (unique_size[i] + total_word[i]))
    return prob
    
def signal_handler(sig, frame):
    print("Exit")
    sys.exit(0)

def insert_trend(time, phrase, trend):
    connection = psycopg.connect(user=DB_USER, dbname=DB_NAME)
    cursor = connection.cursor()               
    query = """INSERT INTO trendiness (cur_t, phrase, trendiness) VALUES (%s,%s,%s)"""
    print("Update score in Postgres")               
    cursor.execute(query, (time, phrase, trend))
    connection.commit()               
    if connection:
        cursor.close()
        connection.close()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--word', type=str)
    args = parser.parse_args()
    exceptions(args.word)
    while True:
        prob = calc_prob(word_count(args.word), all_words_sizes(), unique_sizes())
        print(f"The current time is {get_time()}")
        print(f"The phrase '{args.word}' appears {word_count(args.word)[1]} time(s) in current minute and {word_count(args.word)[0]} time(s) prior to this minute")
        print(f"The trendiness score for '{args.word}' is {math.log10(prob[1]/prob[0])}")
        insert_trend(get_time(), args.word, math.log10(prob[1] + EPSILON/prob[0] + EPSILON))
        time.sleep(10)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    main()
