# Milestone1
Team Project Milestone 1 

Instructions: Please run server.py first, this will parse the text written and timestamped to tweets.txt, then run word_count.py, and finally vocabulary_size.py. 

# Failure.md
In this .md file we talked about some possible failure that may happen when running the code and our recovery logic for resolving potential issues.

# Server.py
In this script, Twitter API's content is transformed to the format of "tweet timestamp in YYYY-MM-DD-HH-MM-SS, tweet text" and stored as tweets.txt. The code will run contiuously after it is started and need to be manually stopped (ctrl + C) to avoid reaching API limit. 

**command line for executing the code (from API)**
```
python server.py
```

**command line for executing the code (from json)** 
```
python server.py --filename jsonfilename.json
```

# Word_count.py
This script allows users to input word or multi-word phrase (maximum limit 2 words) and return the frequency of the word input in all the tweets stored in tweets.txt.
 
**command line for executing the code** 
```
python word_count.py --word "word/phrase"
```

# Vocabulary_size.py
This python script allows users to know how many unique words are there in tweets.txt.

**command line for executing the code** 
```
python vocabulary_size.py
```
