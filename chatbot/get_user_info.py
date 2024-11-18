from flask import request, jsonify
import requests
from dotenv import load_dotenv
import os
import csv
import json
from model.user_model import User

from chatbot.sample import tweet_extraction

# load_dotenv('config/config.env')

def get_user_info_api():

    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    root = "https://ensembledata.com/apis"
    endpoint = "/twitter/user/info"
    params = {
    "name": username,
    "token": os.getenv('ENSEMBLE_API')
    }

    res = requests.get(root+endpoint, params=params)
    
    try:
        print(res.json())

        if res.status_code == 200:
            # Parse the JSON response
            user_info = res.json()

            # Extract rest_id and profile_image_url_https
            rest_id = user_info['data']['rest_id']
            image_url = user_info['data']['legacy']['profile_image_url_https']

            # Specify the output file and folder
            folder_path = "dataset"
            folder = os.path.join(folder_path,username)
            # creating directory if not created
            os.makedirs(folder, exist_ok=True)

            filename2 = f"{rest_id}_info.csv"
            full_path = os.path.join(folder, filename2)
            
            # # Write the JSON data to a text file with pretty formatting
            # with open(full_path, 'w') as file:
            #     file.write(json.dumps(user_info, indent=4))
            

            with open(full_path, 'w', newline='') as file2:
                writer = csv.writer(file2)
                # Writing header
                writer.writerow(["rest_id", "image_url"])
                # Writing the extracted data
                writer.writerow([rest_id, image_url])
            
            # Update the MongoDB user with the new Twitter data
            updated = User.update_user_twitter_info(email, rest_id, image_url)
            
            print(f"User information has been saved to {full_path} in JSON format.")
            tweet_extraction(username,rest_id)
            if updated:
                print(f"User {username} updated successfully with rest_id and profile image URL.")
            else:
                print(f"Failed to update user {username}. User might not exist.")
        else:
            print("error in twitter api",res.status_code)
        
        return jsonify({"message":"User info fetched succussfully"}), 200
    except Exception as e:
        return jsonify({"message":"error in fetching","error":str(e)}),500
