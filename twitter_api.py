from tweepy import OAuthHandler, API, Stream
from tweepy.streaming import StreamListener
import json
import time
import sys
import pandas as pd
import numpy as np
import tweepy
import csv
import psycopg2
from unidecode import unidecode
import os

#import the API keys from the config file, or from Heroku config vars.
try:
    from config import (
        con_key, con_sec, acc_key, acc_sec,
    )
except ModuleNotFoundError:
    con_key = os.environ['CON_KEY']
    con_sec = os.environ['CON_SEC']
    acc_key = os.environ['ACC_KEY']
    acc_sec = os.environ['ACC_SEC']

threat_table = '''CREATE TABLE IF NOT EXISTS unique_threats (
    tweet_id CHAR(19) PRIMARY KEY,
    date TIMESTAMP,
    username VARCHAR,
    is_retweet BOOL,
    is_quote BOOL,
    text VARCHAR,
    quoted_text VARCHAR,
    hashtags TEXT []
); 
'''

def do_query(query_string, *args):
    '''Opens access to Heroku Postgres, executes query,
    commits results, and closes connection.'''
    # Construct connection string and cursor
    DATABASE_URL = os.environ['DATABASE_URL']
    conn = psycopg2.connect(DATABASE_URL, sslmode = 'require')
    cursor = conn.cursor()

    cursor.execute(query_string, *args)
    # Clean up and close out
    conn.commit()
    print('Changes saved.')
    cursor.close()
    conn.close()
    print('Closing out...')

#Popular hashtags extracted from Parler Dataset
popular = [
     'trump2020', 'maga', 'stopthesteal',
     'parler', 'wwg1wga', 'trump',  'kag',
     'truefreespeech', 'qanon', 'maga2020', 
     'voterfraud', 'electionfraud', 'trumptrain',
     'americafirst', 'obamagate', 'keepamericagreat',
     'thegreatawakening', 'parlerusa', 'covid19',
     'draintheswamp',  'fightback',  'patriots',
     'fakenews',  'wethepeople', 'bluelivesmatter',
     '2a', 'antifa', 'donaldtrump', 'truth',
     'democrats', 'kag2020', 'savethechildren',
     'trump2020landslide', 'saveourchildren',
     'wakeupamerica', 'backtheblue', 'deepstate',
     'hangpence', 'walkaway', 
          ]

##transform into hashtags, then boolean format for Streaming object
popular = ['#'+tag for tag in popular]
pop_query = ' OR '.join(popular[:33])

# StreamListener class inherits from tweepy.StreamListener and overrides on_status/on_error methods.
class StreamListener(tweepy.StreamListener):
    def __init__(self, api=None, stop=100):
        from unidecode import unidecode
        import time
        self.api = api
        self.counter = 0
        self.stop = stop
        DATABASE_URL = os.environ['DATABASE_URL']
        self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        self.cursor = self.conn.cursor()

    def db_initpop(self, bundle):
        """
        This function places basic tweet features in the database.  Note the placeholder values:
        these can act as a check to verify that no further expansion was available for that method.
        """
        # unpack the bundle
        tweet_id, created_at, screen_name, is_retweet, is_quote, text, quoted_text, hashtags = bundle
        self.cursor.execute(
            """INSERT INTO unique_threats (tweet_id, date, username, is_retweet, is_quote, text, quoted_text, hashtags)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""", \
            (tweet_id, created_at, screen_name, is_retweet, is_quote, text, quoted_text, hashtags)
        )
        self.conn.commit()
        print('Database populated with tweet ' + str(tweet_id))

    def on_status(self, status):
        self.counter += 1

        if self.counter >= self.stop:
            self.conn.commit()
            self.cursor.close()
            self.conn.close()
            print('Max tweets retrieved. Closing out...')
            return False

        # if "retweeted_status" attribute exists, flag this tweet as a retweet.
        is_retweet = hasattr(status, "retweeted_status")

        # check if text has been truncated
        if hasattr(status, "extended_tweet"):
            text = unidecode(status.extended_tweet["full_text"])
        else:
            text = unidecode(status.text)

        # check if this is a quote tweet.
        is_quote = hasattr(status, "quoted_status")
        quoted_text = ""
        if is_quote:
            # check if quoted tweet's text has been truncated before recording it
            if hasattr(status.quoted_status, "extended_tweet"):
                quoted_text = status.quoted_status.extended_tweet["full_text"]
            else:
                quoted_text = status.quoted_status.text

        print(status.text)
        print('language: ', status.lang)
        print('\n')

        # Add hashtags
        hashtags = [row.get('text') for row in status.entities.get('hashtags')]

        bundle = (
        str(status.id), status.created_at, status.user.screen_name, is_retweet, is_quote, text, quoted_text, hashtags)
        assert len(bundle) == 8, "Bundle is incorrect length"
        self.db_initpop(bundle)
        time.sleep(1)

    def on_error(self, status_code):
        print("Encountered streaming error (", status_code, ")")

        time.sleep(10)
        return False

    def test_rate_limit(self, wait=True, buffer=.1):
        """
        Tests whether the rate limit of the last request has been reached.
        :param api: The `tweepy` api instance.
        :param wait: A flag indicating whether to wait for the rate limit reset
                     if the rate limit has been reached.
        :param buffer: A buffer time in seconds that is added on to the waiting
                       time as an extra safety margin.
        :return: True if it is ok to proceed with the next request. False otherwise.
        """
        # Get the number of remaining requests
        remaining = int(self.api.last_response.getheader('x-rate-limit-remaining'))
        # Check if we have reached the limit
        if remaining == 0:
            limit = int(self.api.last_response.getheader('x-rate-limit-limit'))
            reset = int(self.api.last_response.getheader('x-rate-limit-reset'))
            # Parse the UTC time
            reset = datetime.fromtimestamp(reset)
            # Let the user know we have reached the rate limit
            print
            "0 of {} requests remaining until {}.".format(limit, reset)

            if wait:
                # Determine the delay and sleep
                delay = (reset - datetime.now()).total_seconds() + buffer
                print
                "Sleeping for {}s...".format(delay)
                time.sleep(delay)
                # We have waited for the rate limit reset. OK to proceed.
                return True
            else:
                # We have reached the rate limit. The user needs to handle the rate limit manually.
                return False

                # We have not reached the rate limit
        return True

while True:
    # complete authorization and initialize API endpoint
    auth = tweepy.OAuthHandler(con_key, con_sec)
    auth.set_access_token(acc_key, acc_sec)
    api = tweepy.API(auth)

    # initialize stream
    streamListener = StreamListener(stop = 100)
    stream = tweepy.Stream(auth=api.auth, listener=streamListener,tweet_mode='extended')
    stream.filter(track= ['trump', 'maga', 'wwg1wga'], is_async = True, languages = ['en'])


