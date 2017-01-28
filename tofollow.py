# -*- coding: utf-8 -*-
'''
Author: Soumik Jana soumik.cisco@gmail.com

Description: For a given handle A, scan its following list F, and for each handle in F, find its following list Fi
Combine all such Fi and list all handles followed by at least 10 handles of F, but not by A.

Required Packages: tweepy, argparse, json, prettytable, time

Usage: python tofollow.py -i 'twitter handle'

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

def get_follower_ids(user_id):
    """ Get the list of followers id of a given user using twitter cursor"""
    follower_list = []
    for page in tweepy.Cursor(api.followers_ids, id=user_id, count=5000).pages():
        follower_list += page
        print 'sleeping for a minute after api called GET followers on user id {} to avoid twitter rate limit'.format(user_id)
        time.sleep(60) # For get_followers the rate limit is 15 calls in 15 minutes
    return follower_list

def get_number_of_common_element(list1, list2):
    """ Takes two lists as input and returns the number of common elements
    present in both the lists """
    common_count = 0
    for item1 in list1:
        for item2 in list2:
            if item1 == item2:
                common_count += 1
    return common_count

def if_item_in_list(item, item_list):
    """ Checks if an item is in the list"""
    if item in item_list:
        return True
    return False
                            

if __name__ == "__main__":
    #Parse the argument passed in the commandline
    parser = get_parser()
    args = parser.parse_args()

    #Authenticate Twitter app
    auth = OAuthHandler(config.consumer_key, config.consumer_secret)
    auth.set_access_token(config.access_token,config.access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, retry_count=3, retry_delay=60)

    #Get the id from the user screen_name
    handle_id = api.get_user(args.handle)

    #Get the list of friends ids from the user id
    following_ids = get_following_ids(handle_id._json['id'])

    #Initiate O(n^2) nested loop to get the friends of friends of the user
    for following_id in following_ids:
        for following_of_following_id in get_following_ids(following_id):

            #Get the list of followers for each friends of friends
            follower_ids = get_follower_ids(following_of_following_id) 

            #Get the number of common user between the friends of the user given and the followers of the friend of friend
            common_handle_count = get_number_of_common_element(follower_ids, following_ids)

            #Check if the common user is more than 10 and the given user doesn't follow the friend of friend
            if (common_handle_count >= 10) and (if_item_in_list(handle_id._json['id'], follower_ids) is False):
                following_of_following_user = api.get_user(following_of_following_id)
                t = PrettyTable(['Handle', 'Common Follows', 'Tweets', 'Followers', 'Following'])
                t.add_row([following_of_following_user.screen_name,
                        common_handle_count,
                        following_of_following_user.statuses_count,
                        following_of_following_user.followers_count,
                        following_of_following_user.friends_count])

                print t    

            




        

