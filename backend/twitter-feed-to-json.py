#!/usr/bin/env python
# coding=utf-8

import os, re, sys
from datetime import datetime
import twitter # https://pypi.python.org/pypi/twitter
import pytz # https://pypi.python.org/pypi/pytz
import ConfigParser

# Credits:
# http://stackoverflow.com/questions/4563272/how-to-convert-a-python-utc-datetime-to-a-local-datetime-using-only-python-stand/13287083

def utc_to_local(utc_dt):
    # Convert UTC datetime to local datetime
    local_tz = pytz.timezone('US/Central')
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    return local_tz.normalize(local_dt) # .normalize might be unnecessary

def aslocaltimestr(utc_dt):
    # Reformat local datetime for sign display
    return utc_to_local(utc_dt).strftime('- %A, %B %-d, %-I:%M %p')

def strip_random_ms(text):
    # Remove random millisecond string from tweet text
    return re.sub(r' {[0-9]{1,3}}',r'',text)

def get_last_tweet(twitter_obj, screen_name):
    # Get last tweet from authorized timeline
    last_tweet=twitter_obj.statuses.user_timeline(screen_name=screen_name,
                                                  count=1)[0]
    tweet_text = last_tweet['text']
    tweet_dt = datetime.strptime(last_tweet['created_at'],
                                 '%a %b %d %H:%M:%S +0000 %Y')
    return (tweet_text, tweet_dt)

def get_config(inifile):
    # Read configuration from ini file
    config = ConfigParser.RawConfigParser()
    config.read(inifile)
    return config
    
def setup_twitter(consumer_key, consumer_secret, credentials_file):
    # Authenticate to twitter using OAuth
    if not os.path.exists(credentials_file):
        twitter.oauth_dance("Tweet to Door Sign Converter", consumer_key,
                            consumer_secret, credentials_file)

    oauth_token, oauth_secret = twitter.read_token_file(credentials_file)
    t = twitter.Twitter(auth=twitter.OAuth(
            oauth_token, oauth_secret, consumer_key, consumer_secret))

    return t

def main():
    # Find out where and who we are (in terms of paths and filenames)
    script_dir = os.path.abspath(os.path.dirname(__file__))
    script_file = os.path.basename(os.path.abspath(__file__))
    (script_name, script_ext) = os.path.splitext(script_file)

    # Identify needed files
    credentials_filename = ".%s_app_credentials" % (script_name)
    credentials_file = os.path.join(script_dir, credentials_filename)
    ini_filename = "%s.ini" % (script_name)
    ini_file = os.path.join(script_dir, ini_filename)

    # Get configuration
    config = get_config(ini_filename)
    consumer_key = config.get('twitter', 'CONSUMER_KEY')
    consumer_secret = config.get('twitter', 'CONSUMER_SECRET')
    screen_name = config.get('twitter', 'screen_name')
    graph_url = config.get('graph', 'url')

    # Authenticate to twitter
    t=setup_twitter(consumer_key,consumer_secret,credentials_file)
    # Get last tweet, reformat
    (tweet_text, tweet_dt) = get_last_tweet(t,screen_name)
    reformatted_tweet = "%s %s" % ( strip_random_ms(tweet_text),
                                    aslocaltimestr(tweet_dt) )

    status_filename = "%s.json" % (script_name)
    status_file = os.path.join(script_dir, status_filename)
    reformatted_tweet = '[{"status":"%s", "date":"%s", "graph":"%s"}]' % ( strip_random_ms(tweet_text),
                                     aslocaltimestr(tweet_dt), graph_url )
    with open(status_file, 'w') as f:
        f.write(reformatted_tweet.encode('utf-8'))

if __name__ == "__main__":
    main()
