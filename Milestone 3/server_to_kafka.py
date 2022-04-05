import requests
import json
import time
import argparse
import datetime
import sys
import signal
from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers=['localhost:9092'], api_version=(0,11,5), value_serializer=lambda x: json.dumps(x).encode('utf-8'))

bearer_token = 'AAAAAAAAAAAAAAAAAAAAAKpfUAEAAAAANxOIQpNcy15IBFpyWSttb8dXWuc%3DG0dAjDtnx0nJVckUTi4epzXic1F2gSTmv7y44NhMdOeXJx2zXR'

def create_url():
  return "https://api.twitter.com/2/tweets/sample/stream?tweet.fields=created_at,lang"

def bearer_oauth(r):
  """
  Method required by bearer token authentication.
  """

  r.headers["Authorization"] = f"Bearer {bearer_token}"
  r.headers["User-Agent"] = "v2SampledStreamPython"
  return r
  
def signal_handler(sig, frame):
  print("Exit")
  sys.exit(0)

def clean_info(json_response): 
  timestamp = datetime.datetime.strptime(json_response['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ').strftime("%Y-%m-%d-%H-%M-%S")
  content = json_response['text'].splitlines()
  content = ''.join(str(tweets_data) for tweets_data in content)
  info = {'timestamp': timestamp, 'tweet': content}
  return info

def send_tweer(tweet):
  producer.send('twitter', value=tweet)
  producer.flush()
  # time.sleep(0.5)

def connect_to_endpoint(url):
  response = requests.request("GET", url, auth=bearer_oauth, stream=True)
  for response_line in response.iter_lines():
    if response_line:
      tweet = json.loads(response_line)["data"]
      if tweet['lang'] == "en":
        info = clean_info(tweet)
        if info:
          send_tweer(info)
    if response.status_code != 200:
      raise Exception("Request returned an error: {} {}".format(response.status_code, response.text))

def connect_to_json(filename):
  argsfile = open(filename, "r")
  for i in argsfile:
    tweet = json.loads(argsfile.readline())['data']
    if tweet['lang'] == "en":
      info = clean_info(tweet)
      if info:
        send_tweer(info)      
      
def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--filename', type=str)
  args = parser.parse_args()
  file = args.filename
  if file:
    try:
      connect_to_json(file)
    except:
      print(sys.exc_info()[1])
      sys.exit(1) 
  else:
    try:
      url = create_url()
      connect_to_endpoint(url)
    except:
      print(sys.exc_info()[1])
      sys.exit(1)

if __name__ == "__main__":
  signal.signal(signal.SIGINT, signal_handler)
  main()
