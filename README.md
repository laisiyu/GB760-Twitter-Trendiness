# Milestone03

How to run Milestone03 on your local VM? 

Step 1: Create a database on you local machine by typing psql --username=gb760 --dbname=twitter and then run the SQL code from Milestone2 
```
psql twitter < schema_postgres.sql
```

Step 2: Run all codes in start.sh file to install zookeeper and kafka and kafka-python and to create a topic on Kafka.Install and run everthing in the same order as in the start.sh file on your VM. Leave kafka runnining in the first terminal. 

Step 3: Open new terminals for each py files and run each in the new terminal. In the 2nd one run consumer, in the 3rd one run producer and in the 4th one run trendiness (you can also run producer first and consumer second). 

Step 4: Run the trendiness py file in new terminal. Pick an word, for example "the" and then run the following code: python3 trendiness_kafka.py --word the
then wait a bit to see trendiness of the word in the currnet and previoud minute and so on. 

To stop everything, use control+C in each terminal. 
