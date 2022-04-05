# GB760-Milestone2
In this project, we will build a schema, and insert information that we need to calculate the trendiness score of a word or phrase to psql.

You will need to install psql and psycopg to continue. (If you're using M1 Mac you can install psycopg2 instead)

## Build database

First create a database in postgres on your end, and parse 'schema_postgres.sql' into this database so that two tables named tweets and word_count is created. 
Example Code: 
```
create database dbname
```
```
psql dbname < schema_postgres.sql
```
You can view your existing database using this line 
```
\l
```

## Request server to load data into database

Edit in line 26 and 35 in 'server_postgres.py' to database name and your user name on your postgres end. Then you can run 'server_postgres.py' to request information that we need for calculation from Twitter.api or a json file and load it into the "tweets" table by executing 
```
python server_postgres.py
```
The server will continue to request and load informtion into the database you created until you halt it by pressing control + C or reaching the maximun limits allowed by the API.
**Please run the 'server_postgres.py' at least 2 minutes to collect enough information for calcualtion later.**

## Count the number of a given word/phrase in current minute

In order to use the 'word_count_postgres.py', you need to choose letter, word or any phrase you want to calculate the how many times the word occurred in the current minute. For example, you can try to use this code to calculate how many times word “Apple" occurred in the current minute by
```
python word_count_postgres.py --word Apple
```

## Count the number of unique words in current minute

By using the "vocabulary_size_postgres.py", it would calculate how many unique words occurred in the current minute. You can run the code
```
python vocabulary_size_postgres.py
```

## Compute the trendiness score of a given word/phrase

By using the "trendiness_postgres.py", this ratio tells us the probability of seeing phrase in the current minute at t relative to the probability of seeing the same phrase in the minute prior to t. If the result large and greater than 1, it tells a sudden increase in popularity of that phrase in the current minute. Vice versa, if it less than 1, it tells the phrase lose popularity in the current minute. If it equals to zero, it tells the phrase constant over time. You can run the code 
```
python trendliness_postgres.py -- word "word/phrase"
```
