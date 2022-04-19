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

2.tofollow.py:

Author: Soumik Jana soumik.cisco@gmail.com

Description: For a given handle A, scan its following list F, and for each handle in F, find its following list Fi
Combine all such Fi and list all handles followed by at least 10 handles of F, but not by A.

Required Packages: tweepy, argparse, json, prettytable, time

Usage: python tofollow.py -i 'twitter handle'

Note: Fill up the variable in config.py which contains data path and twitter app credentials.

3.followspy.py:

Author: Soumik Jana soumik.cisco@gmail.com
For a given handle A, scan its following list F, periodically, and report the changes in the F.

Required Packages: tweepy, argparse, json, prettytable, time

Usage: python followspy.py -i 'handle'

Warning: The program runs an infinite loop so don't run it in the background or if you do make sure to kill it after the purpose is achieved.
Note: Fill up the variable in config.py which contains data path and twitter app credentials.

4.visualize_friends_correlation.py:

Author: Soumik Jana soumik.cisco@gmail.com

Description: For a given handle A, scan its following list F, use a ML-learner
and visualize correlations.

Required Packages: tweepy, pandas, argparse, json, sklearn, matplotlib, time

Usage: python visualize_friends_correlation.py -i 'handle'

Note: Fill up the variable in config.py which contains data path and twitter app credentials.
