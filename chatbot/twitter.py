import tweepy
import os
import pandas as pd
import tweepy.errors
from dotenv import load_dotenv

# load_dotenv('config/config.env')

api_key = os.getenv("API_KEY") #Your API/Consumer key 
api_secret = os.getenv("API_SECRET") #Your API/Consumer Secret Key
#these access token is used to authenticate the twitter account so if use these then it is a 2leged 
#authentication so it will only authenticate my account
access_token = os.getenv("ACCESS_TOKEN")    #Your Access token key
access_token_secret = os.getenv("ACCESS_TOKEN_SECRET") #Your Access token Secret key

callback_url = 'http://localhost:8000/twitter/callback'

print(f"api_key:{api_key} and \n api_secret: {api_secret}")
#Pass in our twitter API authentication key
auth = tweepy.OAuth1UserHandler(
    api_key, api_secret,
    access_token, access_token_secret
)

# now this is a 3 legged authentication in which another user will give me the permission to access it's
# public information of the twitter account 
# auth = tweepy.OAuth1UserHandler(
#     api_key, api_secret,
#     callback= callback_url
# )

#Instantiate the tweepy API
api = tweepy.API(auth, wait_on_rate_limit=True)

def tweet_extraction(user_id):
    
    # search_query = "'ref''world cup'-filter:retweets AND -filter:replies AND -filter:links"
    search_query = f"from:{user_id} -filter:retweets AND -filter:replies AND -filter:links"

    no_of_tweets = 2

    try:
        #The number of tweets we want to retrieved from the search
        tweets = api.search_tweets(q=search_query, lang="en", count=no_of_tweets, tweet_mode ='extended')
        
        #Pulling Some attributes from the tweet
        attributes_container = [[tweet.user.name, tweet.created_at, tweet.favorite_count, tweet.source, tweet.full_text] for tweet in tweets]

        #Creation of column list to rename the columns in the dataframe
        columns = ["User", "Date Created", "Number of Likes", "Source of Tweet", "Tweet"]
        
        #Creation of Dataframe
        tweets_df = pd.DataFrame(attributes_container, columns=columns)
        print(tweets_df)
    except BaseException as e:
        print('Status Failed On,',str(e))

def is_valid_user(user_id):
    try:
        user = api.get_user(user_id = user_id)
        return True
    except tweepy.TweepError as e:
        # user not found
        if e.api_code == 50:
            return False
        else:
            print(f"error: {e}")
            return False
        
tweet_extraction('realDonaldTrump')