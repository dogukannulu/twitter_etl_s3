import tweepy
import pandas as pd
import json
from datetime import datetime
import s3fs
from dotenv import dotenv_values

env_vars = dotenv_values(".env")

api_key = env_vars["api_key"]
api_key_secret = env_vars["api_key_secret"]
accesss_token = env_vars["accesss_token"]
accesss_token_secret = env_vars["accesss_token_secret"]