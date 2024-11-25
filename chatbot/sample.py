import requests
from flask import request, jsonify
import json
import csv
import pandas as pd
import os
from chatbot.backend import data_cleaning2


def tweet_extraction(username,rest_id):
    folderpath = f"dataset/{username}"     
    filename = f"{rest_id}_info.csv"
    filepath = os.path.join(folderpath,filename)

    df = pd.read_csv(filepath)
    Id = df['rest_id']
    root = "https://ensembledata.com/apis"
    endpoint = "/twitter/user/tweets"
    params = {
        "id": rest_id,
        "token": os.getenv('ENSEMBLE_API')
    }

    res = requests.get(root + endpoint, params=params)

    # Get the JSON response
    data = res.json()
    print(data)

    # Lists to store the extracted data
    texts = []
    dates = []

    # Extract full_text and created_at from each tweet in the data
    for tweet in data['data']:
        try:
            tweet_data = tweet['content']['itemContent']['tweet_results']['result']['legacy']
            texts.append(tweet_data['full_text'])
            dates.append(tweet_data['created_at'])
        except KeyError:
            continue

    # Create a DataFrame
    df = pd.DataFrame({
        'full_text': texts,
        'created_at': dates
    })

    # Save to CSV
    filename2 = f"{params['id']}_details.csv"
    filepath2 = os.path.join(folderpath,filename2)
    df.to_csv(filepath2, index=False)

    print(f"Data has been written to {filepath2}")
    data_cleaning2(rest_id,username)
