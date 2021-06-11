import tweepy
import json
import preprocessor as p
import pymongo

# MongoDB connector
mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
mongo_db_name = mongo_client["twitter"]
collection = mongo_db_name["tweets"]

# Twitter API Keys
consumer_key = 'Y6IiZcGauAOwBgw39xsFlv9WD'
consumer_secret = 'fZMEiwFjQTtv7sQitkn2heWJvzhuWZnVJbZMVa9INKpZjmWK69'
access_token = '1187760430418145281-x1XcvlInzwaIu0BxBAyIfM7vG2UydV'
access_token_secret = 'PMcpsYvzKlYXAk93ivSEtQzw2qcji59Wr9ai64eS0Hlo9'

# OAuth Authentication and Token Management
authentication = tweepy.OAuthHandler(consumer_key, consumer_secret)
authentication.set_access_token(access_token, access_token_secret)
api = tweepy.API(authentication, wait_on_rate_limit=True,
                 wait_on_rate_limit_notify=True)

# Preprocessor set to remove EMOJI and URL's
p.set_options(p.OPT.EMOJI, p.OPT.URL)


def TwitterSearchAPI(search_term):  # Function to fetch,clean and push tweets to MongoDB from the Search API

    # Keywords to search across Twitter Search Api
    search_keywords = search_term

    # Search API Call with Tweepy to get tweets with search keywords
    tweets = tweepy.Cursor(api.search, q=search_keywords, lang="en", ).items(300)

    for tweet in tweets:
        clean_tweet_text = p.clean(tweet.text)
        tweet_json = (json.loads(json.dumps(tweet._json)))
        tweet_json["text"] = clean_tweet_text
        tweet_json["keyword"] = search_term
        collection.insert_one(tweet_json)