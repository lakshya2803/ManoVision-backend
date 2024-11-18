import pandas as pd
import re
import os
from flask import jsonify
from chatbot.sentiment import analyze_sentiment_for_userApi
    

def data_cleaning():
    # Read the CSV file into a DataFrame
    df = pd.read_csv('dataset/Mental-Health-Twitter.csv')

    # Columns to drop
    to_drop = ['index', 'post_id', 'followers', 'friends', 'favourites', 'statuses', 'retweets', 'label']
    # Remove leading and trailing spaces from column names
    to_drop = [column.strip() for column in to_drop]
    # Check if the columns exist in the DataFrame before dropping them
    for column in to_drop:
        if column in df.columns:
            df.drop(column, axis=1, inplace=True)
        else:
            print(f"Column '{column}' does not exist in the DataFrame.")

    # Apply the clean_text function to the 'post_text' column
    df['post_text'] = df['post_text'].apply(clean_text)
    # Save the cleaned DataFrame to a new CSV file
    df.to_csv('dataset/cleanedData1.csv', index=False)
    print("URLs, words starting with '@', and specified characters have been removed. The cleaned data has been saved to 'cleanedData1.csv'.")

def data_cleaning2(rest_id,username):
    print("Running data_cleaning2 on data")

    folderpath = f'dataset/{username}'
    filename = f'{rest_id}_details.csv'
    filepath = os.path.join(folderpath,filename)
    # Read the CSV file into a DataFrame
    df = pd.read_csv(filepath)

    # Apply the clean_text function to the 'post_text' column
    df['full_text'] = df['full_text'].apply(clean_text)

     # Remove rows where 'full_text' has less than 5 characters
    df['full_text'] = df['full_text'].fillna('')  # Replace NaN with empty strings
    df = df[df['full_text'].str.len() >= 5]

    # Convert 'created_at' column to datetime and format it to show only Month and Day
    df['created_at'] = pd.to_datetime(df['created_at'], format='%a %b %d %H:%M:%S %z %Y',errors='coerce')

    #sort the dataframe
    df = df.sort_values(by='created_at').reset_index(drop=True)

    # convert the date in desired format
    df['created_at'] = df['created_at'].dt.strftime('%d %b %y')

    # Save the cleaned DataFrame to a new CSV file
    filename2 = f'{rest_id}_cleandata.csv'
    filepath2 = os.path.join(folderpath,filename2)
    df.to_csv(filepath2, index=False)
    print(f"URLs, words starting with '@', and specified characters have been removed. The cleaned data has been saved to {filepath2}.")

    # calling the vader for sentiment analysis
    analyze_sentiment_for_userApi(rest_id,username)

# Function to remove URLs, words starting with '@', and specified characters from text
def clean_text(text):
    # Use regular expressions to match and remove URLs, words starting with '@', 
    # and specified characters jese ke :-- 
    cleaned_text = re.sub(r'http[s]?://\S+|\@\w+|:|"|\'|―|#', '', text)
    return cleaned_text
