#this project is created by Aryan Khandelwal (github.com/ark4112)

import tweepy
import pandas as pd
import time
import re
import matplotlib.pyplot as plt
from textblob import TextBlob

#Access credentials from developer.twitter.com
consumer_key = 'c3gdGgI2UpCCKHZ2JplBIS2px'
consumer_secret = 'ayM7DSrmEHrdwO8M4FNoHowYY95lFyh5frpyJogVO89A5fFdY7'
access_token_key = '2613493670-YzWIuHAwtnVVNoBMnyVDonY82F0mEzwW2Omht6p'
access_token_secret = 'S15Ia5GkKf4Jk9svJzXVnaRUdEiLzmXdd0fTHmVCpHJBO'

#Get an authentication object for accessing Twitter Rest API using Application Only Auth(Max Rate of fetching=45000 tweets/15 minutes)
auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
#Get an API obect using authentication object
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

#Function to remove URL from tweets
def remove_url(txt):
    """Replace URLs found in a text string with nothing 
    (i.e. it will remove the URL from the string).

    Parameters
    ----------
    txt : string
        A text string that you want to parse and remove urls.

    Returns
    -------
    The same txt string with url's removed.
    """

    return " ".join(re.sub("([^0-9A-Za-z \t])|(\w+:\/\/\S+)", "", txt).split())

#search query title
search_term = "#COVID -filter:retweets"

#Fetching tweets and Handling pagination 
tweets = tweepy.Cursor(api.search,
                   q=search_term,
                   lang="en",
                   since='2020-03-01').items(1000)

# Remove URLs
tweets_no_urls = [remove_url(tweet.text) for tweet in tweets]

# Create textblob objects of the tweets
sentiment_objects = [TextBlob(tweet) for tweet in tweets_no_urls]

#Return polarity values in range of [-1.0,1.0]
sentiment_objects[0].polarity, sentiment_objects[0]

#create a list of tweets and their polarity values
sentiment_values = [[tweet.sentiment.polarity,
                     str(tweet)] for tweet in sentiment_objects]
sentiment_values[0]

#Create a Pandas DataFrame(Similar to tabular data)
sentiment_df = pd.DataFrame(sentiment_values, columns=["polarity", "tweet"])
#Return 1000 rows of the data frame
sentiment_df.head(1000)

#remove the polarity values equal to zero
sentiment_df = sentiment_df[sentiment_df.polarity != 0]

#Defining size of histogram 8*6
fig, ax = plt.subplots(figsize=(8, 6))

# Plot histogram of the polarity values
sentiment_df.hist(bins=[-1, -0.75, -0.5, -0.25,0.0,0.25, 0.5, 0.75, 1],ax=ax,
                  color="purple")

#Defining title of the histogram
plt.title("Sentiments from Tweets on COVID-19")
#Diiplay Histogram
plt.show()


#End Of program
