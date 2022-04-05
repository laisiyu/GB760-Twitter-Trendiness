import word_count_postgres as w

def get_all_words(text_list):
  all_words = []
  for tweet in text_list:
    words = tweet.strip().split()
    for i in words:
      all_words.append(i)
  return all_words

def main():
    time = w.get_time()
    text_list = w.get_all_tweets(time,1)
    clean_text_list = w.clean_text(text_list)
    all_words = get_all_words(clean_text_list)
    vocab_size = len(set(all_words))
    print(f"The vocabulary size is {vocab_size}")

if __name__ == "__main__":
  main()
