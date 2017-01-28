# -*- coding: utf-8 -*-
'''
Author: Soumik Jana soumik.cisco@gmail.com

Description: Scan the latest twitter feeds originating from a particular country for a given hashtag, using Twitter’s Streaming API.
The program creates a file which stores raw twitter streams with the name stream_<query given as argument>.json at the data path mentioned in the config.py file
for testing purposes.

Required Packages: tweepy, argparse, time, string, json, prettytable

Usage: python scantag.py -q 'hashtag' -c 'country'

Note: Fill up the variable in config.py which contains data path and twitter app credentials.
'''
#Importing config from config.py
import config

#Import the necessary methods from tweetir API library
import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

#Importing argparse for parsing argument passed to the script
import argparse

#Importing time
import time

#Importing string
import string

#Importing json
import json

#Importing prettytable for tabular output
from prettytable import PrettyTable


def get_parser():
    """Get parser for command line arguments."""
    parser = argparse.ArgumentParser(description="Scanning Twitter Stream")
    parser.add_argument("-q",
                        "--query",
                        dest="query",
                        help="Query/Filter",
                        default='-')
    parser.add_argument("-c",
                        "--country",
                        dest="country",
                        help="Country/Location",
			default='India')
    return parser

def checkJson(jsonContents):
    """ Check if the json value for key 'place' and 'country' exists"""

    placeFlag = True if 'place' in jsonContents and jsonContents["place"] is not None else False
    if placeFlag is True:
        countryFlag = True if 'country' in jsonContents["place"] and jsonContents["place"]["country"] is not None else False
    else:
        countryFlag = False
    return countryFlag

class MyListener(StreamListener):
    """Custom StreamListener for streaming data."""

    def __init__(self, query):
        query_fname = format_filename(query)
        self.outfile = "%s/stream_%s.json" % (config.data_dir, query_fname)
        self.t = PrettyTable(['Handle', 'Date', 'Rts', 'Likes', 'Tweet'])

    def on_data(self, data):
        try:
            with open(self.outfile, 'a') as f:
                decoded = json.loads(data)
                f.write(json.dumps(decoded, indent=4, sort_keys=True))
                if checkJson(decoded) is True:
                    if (decoded['place']['country'] == args.country):
                        self.t.add_row([decoded['user']['screen_name'],
                                        decoded['created_at'],
                                        decoded['retweet_count'],
                                        decoded['favorite_count'],
                                        decoded['text']])
                        print self.t
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
            time.sleep(5)
        return True

    def on_error(self, status):
        print(status)
        return True
    
def format_filename(fname):
    """Convert file name into a safe string.
    Arguments:
    fname -- the file name to convert
    Return:
    String -- converted file name
    """
    return ''.join(convert_valid(one_char) for one_char in fname)

def convert_valid(one_char):
    """Convert a character into '_' if invalid.
    Arguments:
    one_char -- the char to convert
    Return:
    Character -- converted char
    """
    valid_chars = "-_.%s%s" % (string.ascii_letters, string.digits)
    if one_char in valid_chars:
        return one_char
    else:
        return '_'

@classmethod
def parse(cls, api, raw):
    status = cls.first_parse(api, raw)
    setattr(status, 'json', json.dumps(raw))
    return status
#To get geolocated tweets finding the boundingbox for a country. UPDATE: Not the requirement
'''
def get_country_position(country):
    url_query=[]
    url_query.append('country={}'.format(country))
    url = u'http://nominatim.openstreetmap.org/search?'
    url += '&'.join(url_query)
    url += '&format=json&polygon=0'
    results = urllib.urlopen(url).read()
    result_string = json.loads(results)
    result_float = map(float,result_string[0]['boundingbox'])
    sw_lon = result_float[2]
    sw_lat = result_float[0]
    ne_lon = result_float[3]
    ne_lat = result_float[1]
    return [sw_lon,sw_lat,ne_lon,ne_lat]
'''
if __name__ == '__main__':
    #Parse the argument given in the commandline
    parser = get_parser()
    args = parser.parse_args()

    #Authenticate Twitter app
    auth = OAuthHandler(config.consumer_key, config.consumer_secret)
    auth.set_access_token(config.access_token,config.access_token_secret)
    api = tweepy.API(auth)

    #Get the Twitter stream data
    twitter_stream = Stream(auth, MyListener(args.query))

    #Filter the Twitter stream based on the query passed as argument
    twitter_stream.filter(track=[args.query])





