# -*- coding: utf-8 -*-
'''
Author: Soumik Jana soumik.cisco@gmail.com

For a given handle A, scan its following list F, periodically, and report the changes in the F.

Required Packages: tweepy, argparse, json, prettytable, time

Usage: python followspy.py -i 'handle'

Warning: The program runs an infinite loop so don't run it in the background or if you do make sure to kill it after the purpose is achieved.

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

#Importing simple json
import json

#Importing prettytable for tabular output
from prettytable import PrettyTable

#Importing Time
import time

def get_parser():
    """Get parser for command line arguments."""
    parser = argparse.ArgumentParser(description="To Follow")
    parser.add_argument("-i",
                        "--id",
                        dest="handle",
                        help="Id/Handle",
                        default="sojana")
    return parser

def get_following_ids(user_id):
    """ Get the list of friends id of a given user using twitter cursor"""
    following_ids = []
    for user in tweepy.Cursor(api.friends_ids, id=user_id, count=5000).pages():
        following_ids += user
        print 'sleeping for a minute after api called GET friends on user id {} to avoid twitter rate limit'.format(user_id)
        time.sleep(60) # For get_friends the rate limit is 15 calls in 15 minutes
    return following_ids

def get_deleted_friends(pre_list, post_list):
    """Compare two lists and return list of items which are not present in the later list """
    return_list = []
    for pre_id in pre_list:
        if pre_id not in post_list:
            return_list.append(pre_id)
    return return_list

def get_added_friends(pre_list, post_list):
    """Compare two lists and return list of items which are added new in the later list """
    return_list = []
    for post_id in post_list:
        if post_id not in pre_list:
            return_list.append(post_id)
    return return_list

if __name__ == "__main__":
    #Parse the argument passed in the commandline
    parser = get_parser()
    args = parser.parse_args()

    #Authenticate Twitter app
    auth = OAuthHandler(config.consumer_key, config.consumer_secret)
    auth.set_access_token(config.access_token,config.access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, retry_count=3, retry_delay=60)

    #Get the id of the given user from the screen_name
    handle_id = api.get_user(args.handle)

    #Initiate an infinite loop
    while True:
        #Get initial list of friends ids 
        pre_following_ids = get_following_ids(handle_id._json['id'])

        #Sleep for 5 minutes before again getting the list of friends ids
        print 'Sleeping for five minutes before retrieving friends list for {} again'.format(args.handle)
        time.sleep(300)

        #Get the list of friends ids after 5 minutes to check any changes took place
        post_following_ids = get_following_ids(handle_id._json['id'])
        deleted_friends_list = get_deleted_friends(pre_following_ids, post_following_ids)
        added_friends_list = get_added_friends(pre_following_ids, post_following_ids)
        if not deleted_friends_list and not added_friends_list:
            print 'no changes seen in friends lists for {}\'s friends list'.format(args.handle)
        else:
            t = PrettyTable(['Handle', 'Action', 'Tweets', 'Followers', 'Following'])
            if deleted_friends_list:
                for deleted_id in deleted_friends_list:
                    deleted_user = api.get_user(deleted_id)
                    t.add_row([deleted_user.screen_name, 
                            'Del',
                            deleted_user.statuses_count,
                            deleted_user.followers_count,
                            deleted_user.friends_count])
            if added_friends_list:
                for added_id in added_friends_list:
                    added_user = api.get_user(added_id)
                    t.add_row([added_user.screen_name, 
                            'Add',
                            added_user.statuses_count,
                            added_user.followers_count,
                            added_user.friends_count])
            print t

            




        

