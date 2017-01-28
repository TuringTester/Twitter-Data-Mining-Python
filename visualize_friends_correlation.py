# -*- coding: utf-8 -*-
'''
Author: Soumik Jana soumik.cisco@gmail.com

Description: For a given handle A, scan its following list F, use a ML-learner
and visualize correlations.

Required Packages: tweepy, pandas, argparse, json, sklearn, matplotlib, time

Usage: python visualize_friends_correlation.py -i 'handle'

Note: Fill up the variable in config.py which contains data path and twitter app credentials.
'''
#Importing pandas to use data frames
import pandas as pd

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

# Import matplotlib
import matplotlib.pyplot as plt

# Import the kmeans clustering model.
from sklearn.cluster import KMeans

# Import the PCA model.
from sklearn.decomposition import PCA

#Importing time
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

def get_following_users(user_id):
    """ Get the list of friends user object of a given user using twitter cursor"""

    following_users = []
    for user in tweepy.Cursor(api.friends, id=user_id, count=200).pages():
        following_users += user
        print 'sleeping for a minute after api called GET friends on user id {} to avoid twitter rate limit'.format(user_id)
        time.sleep(60) # For get_friends the rate limit is 15 calls in 15 minutes
    return following_users

def checkJson(jsonContents):
    """ Check if the json value for key 'place' and 'country' exists"""

    placeFlag = True if 'place' in jsonContents and jsonContents["place"] is not None else False
    if placeFlag is True:
        countryFlag = True if 'country' in jsonContents["place"] and jsonContents["place"]["country"] is not None else False
    else:
        countryFlag = False
    return countryFlag

if __name__ == "__main__":
    #Parsing arguments given in the commandline
    parser = get_parser()
    args = parser.parse_args()

    #Authenticate Twitter app
    auth = OAuthHandler(config.consumer_key, config.consumer_secret)
    auth.set_access_token(config.access_token,config.access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, retry_count=3, retry_delay=60)

    #Get the id from the screen_name of the given user
    handle_id = api.get_user(args.handle)

    #Get friends user object list
    following_users = get_following_users(handle_id._json['id'])

    #Convert list of user object to list of json
    following_users_json = []
    for user in following_users:
        following_users_json.append(user._json)

    #Create data frame from the list of json
    friends_data = pd.DataFrame()
    friends_data['screen_name'] = map(lambda user: user['screen_name'], following_users_json)
    friends_data['statuses_count'] = map(lambda user: user['statuses_count'], following_users_json)
    friends_data['followers_count'] = map(lambda user: user['followers_count'], following_users_json)
    friends_data['friends_count'] = map(lambda user: user['friends_count'], following_users_json)
    friends_data['lang'] = map(lambda user: user['lang'], following_users_json)
    friends_data['country'] = map(lambda user: user['place']['country'] if checkJson(user) is True else None, following_users_json)
    
    # Initialize the model with 2 parameters -- number of clusters and random state.
    kmeans_model = KMeans(n_clusters=5, random_state=1)

    # Get only the numeric columns from friends_data.
    good_columns = friends_data._get_numeric_data()

    # Fit the model using the good columns.
    kmeans_model.fit(good_columns)

    # Get the cluster assignments.
    labels = kmeans_model.labels_

    # Create a PCA model.
    pca_2 = PCA(2)
    
    # Fit the PCA model on the numeric columns from earlier.
    plot_columns = pca_2.fit_transform(good_columns)

    # Make a scatter plot of each user, shaded according to cluster assignment.
    plt.scatter(x=plot_columns[:,0], y=plot_columns[:,1], c=labels)

    # Show the plot.
    plt.show()
    
 
        


            




        

