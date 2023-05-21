import tweepy
import pandas as pd
import json
import logging
from datetime import datetime
import s3fs
from dotenv import dotenv_values

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s:%(funcName)s:%(levelname)s:%(message)s')

env_vars = dotenv_values(".env")

api_key = env_vars["api_key"]
api_key_secret = env_vars["api_key_secret"]
accesss_token = env_vars["accesss_token"]
accesss_token_secret = env_vars["accesss_token_secret"]

try:
    auth = tweepy.OAuthHandler(api_key, api_key_secret)
    auth.set_access_token(accesss_token, accesss_token_secret)

    api = tweepy.API(auth)
    logging.info('Tweepy API object created successfully')
except Exception as e:
    logging.error(f"The Tweepy API object cannot be created dur to: {e}")

def get_twitter_timeline():
    """
    Gets the 200 latest tweets of a specific Twitter user.
    """
    tweets = api.user_timeline(screen_name='@elonmusk', 
                            count=200,
                            include_rts = False,
                            tweet_mode = 'extended'
                            )

    return tweets


def create_tweet_list(tweets):
    tweet_list = []
    for tweet in tweets:
        text = tweet._json["full_text"]

        refined_tweet = {"user": tweet.user.screen_name,
                        'text' : text,
                        'favorite_count' : tweet.favorite_count,
                        'retweet_count' : tweet.retweet_count,
                        'created_at' : tweet.created_at}
        
        tweet_list.append(refined_tweet)
    
    return tweet_list


def download_tweets_as_csv(tweet_list):
    df = pd.DataFrame(tweet_list)

    return df.to_csv('s3://my_bucket_name/elon_tweets.csv')


def main():
    tweets = get_twitter_timeline()
    tweet_list = create_tweet_list(tweets)
    download_tweets_as_csv(tweet_list)
