import pandas as pd
import os
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from model.user_model import User  


def analyze_sentiment_for_user(user_id):
    # Read the CSV file into a DataFrame
    df = pd.read_csv("cleanedData1.csv")

    # Filter DataFrame for the specified user_id
    user_df = df[df['user_id'] == user_id]

    if user_df.empty:
        print(f"No data found for user {user_id}.")
        return

    # Initialize the VADER sentiment analyzer
    analyzer = SentimentIntensityAnalyzer()

    # Create lists to store the data
    data_list = []

    # Create a dictionary to store user-specific sentiment scores
    user_sentiment_scores = {}

    # Group the data by user_id (although there's only one user now)
    grouped = user_df.groupby('user_id')

    for _, group in grouped:
        # Initialize lists to store sentiment scores for the user's posts
        compound_scores = []

        for post_text in group['post_text']:
            # Perform VADER sentiment analysis on each post
            sentiment_scores = analyzer.polarity_scores(post_text)
            compound_scores.append(sentiment_scores['compound'])

        # Calculate the average sentiment score for the user
        average_score = sum(compound_scores) / len(compound_scores)

        # Store the user's average sentiment score in the dictionary
        user_sentiment_scores[user_id] = average_score

        # Append user's data to the data_list
        for post_text, sentiment_score in zip(group['post_text'], compound_scores):
            data_list.append([user_id, post_text, sentiment_score])

    # Create a DataFrame with the collected data
    analyzed_df = pd.DataFrame(data_list, columns=['user_id', 'post_text', 'sentiment_score'])

    # Save the DataFrame to a new CSV file
    analyzed_df.to_csv(f"analyzedDataFinalProduct2_{user_id}.csv", index=False)

    # Create a DataFrame for unique user_id and average_sentiment_score
    all_sentiment_scores_df = pd.DataFrame(list(user_sentiment_scores.items()), columns=['user_id', 'average_sentiment_score'])

    # Save the DataFrame to a new CSV file
    all_sentiment_scores_df.to_csv(f"all_sentiment_score3_{user_id}.csv", index=False)

    # Display the results
    for user_id, avg_score in user_sentiment_scores.items():
        print(f"User {user_id}: Average Sentiment Score = {avg_score:.2f}")
        return avg_score

def analyze_sentiment_for_userApi(rest_id,username):

    folderpath = f'/tmp/dataset/{username}'  #made a change
    filename = f'{rest_id}_cleandata.csv'
    filepath = os.path.join(folderpath,filename)
    # Read the CSV file into a DataFrame
    df = pd.read_csv(filepath)

    
    # Initialize the VADER sentiment analyzer
    analyzer = SentimentIntensityAnalyzer()

    # Create lists to store the data
    data_list = []

    # Create a dictionary to store user-specific sentiment scores
    user_sentiment_scores = {}

    # Initialize lists to store sentiment scores for the user's posts
    compound_scores = []

    for post_text,created_at in zip(df['full_text'], df['created_at']):
            # Perform VADER sentiment analysis on each post
        sentiment_scores = analyzer.polarity_scores(post_text)
        compound_scores.append(sentiment_scores['compound'])

        # Calculate the average sentiment score for the user
        average_score = sum(compound_scores) / len(compound_scores)

        # Store the user's average sentiment score in the dictionary
        user_sentiment_scores[rest_id] = average_score

        # Append user's data to the data_list
        for post_text, sentiment_score in zip(df['full_text'], compound_scores):
            data_list.append([rest_id, post_text, created_at, sentiment_score])

    # Create a DataFrame with the collected data
    analyzed_df = pd.DataFrame(data_list, columns=['rest_id', 'post_text', 'created_at', 'sentiment_score'])

    # Save the DataFrame to a new CSV file
    filename2 = f"analyzedDataFinalProduct_{rest_id}.csv"
    filepath2 = os.path.join(folderpath,filename2)
    analyzed_df.to_csv(filepath2, index=False)

    # Create a DataFrame for unique user_id and average_sentiment_score
    all_sentiment_scores_df = pd.DataFrame(list(user_sentiment_scores.items()), columns=['rest_id', 'average_sentiment_score'])

    for Id,avg in user_sentiment_scores.items():
        updated_user = User.add_twitter_score(Id,avg)

    # Save the DataFrame to a new CSV file
    filename3 = f"all_sentiment_score_{rest_id}.csv"
    filepath3 = os.path.join(folderpath,filename3)
    all_sentiment_scores_df.to_csv(filepath3, index=False)

    # # Display the results
    # for user_id, avg_score in user_sentiment_scores.items():
    #     print(f"User {user_id}: Average Sentiment Score = {avg_score:.2f}")
    #     return avg_score
    