import word_count as w

def get_all_words(text_list):
    all_words = []
    for tweet in text_list:
      words = tweet.strip().split()
      for i in words:
        all_words.append(i)
    return all_words

def main():
    all_words = get_all_words(w.all_tweets())
    vocab = set(all_words)
    print(f"There are '{len(vocab)}' unique words")

if __name__ == "__main__":
    main()
