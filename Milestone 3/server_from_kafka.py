from kafka import KafkaConsumer
from json import loads
import signal
import sys
import psycopg

DB_USER = 'gb760'
DB_NAME = 'twitter'

consumer = KafkaConsumer(
    'twitter',
     bootstrap_servers=['localhost:9092'],
     api_version=(0,11,5),
     auto_offset_reset='earliest',
     enable_auto_commit=True,
     value_deserializer=lambda x: loads(x.decode('utf-8')))

def reset_tweets():
    connection = psycopg.connect(user=DB_USER, dbname=DB_NAME)
    cursor = connection.cursor()
    cursor.execute("""TRUNCATE tweets""")
    connection.commit()
    if connection:
        cursor.close()
        connection.close()

def insert_info(tweet):
    print(tweet)
    connection = psycopg.connect(user=DB_USER, dbname=DB_NAME)
    cursor = connection.cursor()               
    query = """INSERT INTO tweets (time_stamp, content) VALUES (%s,%s)"""
    cursor.execute(query, (tweet['timestamp'], tweet['tweet']))
    connection.commit()               
    if connection:
        cursor.close()
        connection.close()
             
def signal_handler(sig, frame):
    print("Exit")
    sys.exit(0)

reset_tweets()
signal.signal(signal.SIGINT, signal_handler)
for message in consumer:
    message = message.value
    insert_info(message)
