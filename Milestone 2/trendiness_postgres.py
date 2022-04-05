import argparse
import math
import word_count_postgres as w
import psycopg

EPSILON = 0.0000001

def get_all_words(text_list):
  all_words = []
  for tweet in text_list:
    words = tweet.strip().split()
    for i in words:
      all_words.append(i)
  return all_words

def word_count(word):
    count_in_minutes = []
    for i in range(2):
        all_words = w.clean_text(w.get_all_tweets(w.get_time(),i))
        count_in_minutes.append(w.countnum(word, all_words))
    return count_in_minutes

def unique_sizes():
    unique_sizes_in_minutes = []
    for i in range(2):
        text = get_all_words(w.clean_text(w.get_all_tweets(w.get_time(),i)))
        size = len(set(text))
        unique_sizes_in_minutes.append(size)
    return unique_sizes_in_minutes

def all_words_sizes():
    all_sizes_in_minutes = []
    for i in range(2):
        text = get_all_words(w.clean_text(w.get_all_tweets(w.get_time(),i)))
        size = len(text)-text.count('')
        all_sizes_in_minutes.append(size)
    return all_sizes_in_minutes

def calc_prob(count, total_word, unique_size):
    prob = []
    for i in range(2):
        prob.append((1+count[i]) / (unique_size[i] + total_word[i]))
    return prob
    
def insert_trend(time, phrase, trend):
    connection = psycopg.connect(user="gb760", dbname = "twitter")
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
    w.exceptions(args.word)
    # print(word_count(args.word))
    # print("unique size", unique_sizes())
    # print("all words", all_words_sizes())
    # print(calc_prob(word_count('i'), all_words_sizes(), unique_sizes()))
    prob = calc_prob(word_count(args.word), all_words_sizes(), unique_sizes())
    print(f"The current time is {w.get_time()}")
    print(f"The phrase '{args.word}' appears {word_count(args.word)[1]} time(s) in current minute and {word_count(args.word)[0]} time(s) prior to this minute")
    print(f"The trendiness score for '{args.word}' is {math.log10(prob[1]/prob[0])}")
    insert_trend(w.get_time(), args.word, math.log10((prob[1] + EPSILON)/(prob[0]+ EPSILON)))

if __name__ == "__main__":
  main()
