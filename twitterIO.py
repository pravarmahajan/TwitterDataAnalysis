import re

import twitter
import json

import twitter_config

def stream_and_save_twitter_data(twitter_count):

    oauth = twitter.OAuth(twitter_config.ACCESS_TOKEN,
                          twitter_config.ACCESS_SECRET,
                          twitter_config.CONSUMER_KEY,
                          twitter_config.CONSUMER_SECRET)
    twitter_stream = twitter.TwitterStream(auth=oauth)
    iterator = twitter_stream.statuses.sample()

    twitter_data_array = []
    for tweet in iterator:
        twitter_count -= 1
        twitter_data_array.append(tweet)
        if twitter_count <= 0:
            break

    twitter_data_file = open(twitter_config.twitter_data_filename, "w")
    json.dump(twitter_data_array, twitter_data_file, indent=4,
              separators=(",", ":")
    )
    twitter_data_file.close()

def load_twitter_data_from_file(twitter_count):
    twitter_data_file = open(twitter_config.twitter_data_filename, "r")
    twitter_data = json.load(twitter_data_file)
    twitter_data_file.close()
    return twitter_data

def remove_RT(tweet_text):
    RT_regex = "^RT "
    tweet_text = re.sub(RT_regex, "", tweet_text)
    return tweet_text

def remove_hashtag(tweet_text):
    hashtag_regex = "#[A-Za-z0-9_]+"
    tweet_text = re.sub(hashtag_regex, "", tweet_text)
    return tweet_text
    
def remove_at_username(tweet_text): #removes @username
    at_username_regex = "@[A-Za-z0-9_]+"
    tweet_text = re.sub(at_username_regex, "", tweet_text)
    return tweet_text

def process_single_tweet(tweet):
    tweet['text'] = remove_RT(tweet['text'])
    tweet['text'] = remove_hashtag(tweet['text'])
    tweet['text'] = remove_at_username(tweet['text'])
    tweet['text'] = tweet['text'].strip()
    return tweet

def process_twitter_data(twitter_data):
    twitter_data = [tweet for tweet in twitter_data
                    if 'text' in tweet.keys()] #removes non text tweets
    twitter_data = map(process_single_tweet, twitter_data)

    return twitter_data
