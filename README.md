# twitter_data_mining
Four command-line tools for twitter data mining. 

1. scantag.py:
Author: Soumik Jana soumik.cisco@gmail.com

Description: Scan the latest twitter feeds originating from a particular country for a given hashtag, using Twitter’s Streaming API.
The program creates a file which stores raw twitter streams with the name stream_<query given as argument>.json at the data path mentioned in the config.py file
for testing purposes.

Required Packages: tweepy, argparse, time, string, json, prettytable

Usage: python scantag.py -q 'hashtag' -c 'country'

Note: Fill up the variable in config.py which contains data path and twitter app credentials.
