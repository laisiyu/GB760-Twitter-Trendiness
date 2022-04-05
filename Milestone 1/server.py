import requests
import json
import argparse
import datetime
import sys
import signal

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

def connect_to_endpoint(url):
  response = requests.request("GET", url, auth=bearer_oauth, stream=True)
  for response_line in response.iter_lines():
    if response_line:
      tweet = json.loads(response_line)["data"]
      lang = tweet['lang']
      if lang == "en":
        with open("tweets.txt", "a") as file:
          timestamp = datetime.datetime.strptime(
              tweet['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ').strftime("%Y-%m-%d-%H-%M-%S")
          text = tweet['text'].splitlines()
          text = ''.join(str(tweets_data) for tweets_data in text)
          file.write(f"{timestamp}, {text}\n")
        file.close()
    if response.status_code != 200:
      raise Exception("Request returned an error: {} {}".format(
          response.status_code, response.text))

def connect_to_json(filename):
  argsfile = open(filename, "r")
  for i in argsfile:
    tweets = json.loads(argsfile.readline())
    with open('tweets.txt', 'a') as file:
      timestamp = datetime.datetime.strptime(
          tweets['data']['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ').strftime("%Y-%m-%d-%H-%M-%S")
      text = tweets['data']['text'].splitlines()
      text = ''.join(str(tweets_data) for tweets_data in text)
      file.write(f"{timestamp}, {text}\n")
      file.close()

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--filename', type=str)
  args = parser.parse_args()
  if args.filename:
    try:
      connect_to_json(args.filename)
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
