import tweepy
import os
import pandas as pd
import tweepy.errors
from flask import jsonify, session, request

api_key = os.getenv("API_KEY") #Your API/Consumer key 
api_secret = os.getenv("API_SECRET") #Your API/Consumer Secret Key

client_id = os.getenv('CLIENT_ID') # PROJECT'S client id
client_secret = os.getenv('CLIENT_SECRET') # Project's client secret key

#these access token is used to authenticate the twitter account so if use these then it is a 2leged 
#authentication so it will only authenticate my account
# access_token = os.getenv("ACCESS_TOKEN")    #Your Access token key
# access_token_secret = os.getenv("ACCESS_TOKEN_SECRET") #Your Access token Secret key

callback_url = 'http://localhost:5173/questions' #change this url as per the frontend

#Pass in our twitter API authentication key
# auth = tweepy.OAuth1UserHandler(
#     api_key, api_secret,
#     access_token, access_token_secret
# )

# now this is a 3 legged authentication in which another user will give me the permission to access it's
# public information of the twitter account 
auth = tweepy.OAuth2UserHandler(
    client_id=client_id,
    redirect_uri= callback_url,
    scope=["tweet.read", "users.read", "offline.access"],
    client_secret=client_secret
)


def twitter_login():
    try:
        redirect_url = auth.get_authorization_url()
        # session['request_token'] = auth.request_token
        return jsonify({'auth_url' : redirect_url}), 200
    except Exception as e:
        return jsonify({"error":f"failed to get request url {str(e)}"}), 500

def twitter_callback():
    code = request.args.get('code')
    if not code:
        return jsonify({'error': 'No authorization code provided'}), 400

    try:
        # Exchange the authorization code for access token
        auth.fetch_token(code=code)
        access_token = auth.access_token

        # Initialize Tweepy API client with the access token
        api = tweepy.Client(bearer_token=access_token)

        # Get user info
        user = api.get_me()
        
        return jsonify({
            'name': user.data.name,
            'username': user.data.username,
            'profile_image_url': user.data.profile_image_url,
            'followers_count': user.data.public_metrics['followers_count'],
            'location': user.data.location,
            'description': user.data.description
        }), 200
    except Exception as e:
        return jsonify({'error': f'Failed to get access token: {str(e)}'}), 500 


def user_tweets():
    # Check if access tokens are available in the session
    access_token = session.get('access_token')
    access_token_secret = session.get('access_token_secret')

    if not access_token or not access_token_secret:
        return jsonify({'error': 'User is not authenticated'}), 401  # Unauthorized

    try:
        # Initialize Tweepy API object with stored access token and secret
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)

        # Fetch the latest 5 tweets from the authenticated user's timeline
        tweets = api.user_timeline(count=5, tweet_mode="extended")

        tweet_data = []
        for tweet in tweets:
            tweet_data.append({
                'text': tweet.full_text,
                'created_at': tweet.created_at,
                'retweet_count': tweet.retweet_count,
                'favorite_count': tweet.favorite_count,
            })

        return jsonify(tweet_data), 200

    except tweepy.TweepError as e:
        return jsonify({'error': f'Failed to fetch tweets: {str(e)}'}), 500
    

bearer_token = os.getenv("BEARER_TOKEN")

# Initialize Tweepy client with Bearer Token
client = tweepy.Client(bearer_token=bearer_token)

def get_user_tweets():
    try:
        # Fetch user details to get the user ID
        username = request.view_args.get('username')
        user = client.get_user(username=username)
        if not user.data:
            return jsonify({'error': 'User not found'}), 404

        user_id = user.data.id

        # Fetch recent tweets by user ID (adjust `max_results` as needed)
        tweets = client.get_users_tweets(id=user_id, max_results=2)

        # Collect tweet details
        tweet_data = []
        if tweets.data:
            for tweet in tweets.data:
                tweet_data.append({
                    'tweet_id': tweet.id,
                    'text': tweet.text,
                    'created_at': tweet.created_at
                })

        return jsonify({'tweets': tweet_data}), 200

    except tweepy.TweepyException as e:
        return jsonify({'error': f'Failed to fetch tweets: {str(e)}'}), 500
    
