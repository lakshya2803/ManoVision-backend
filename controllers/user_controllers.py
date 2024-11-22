from model.user_model import User
from flask import jsonify, request
import os
import pandas as pd
from datetime import datetime, timedelta
import jwt
# from chatbot.twitter import is_valid_user

def sign_up():
    try:
        data = request.get_json()
        name = data.get("name")
        email = data.get("email")
        password = data.get("password")
        gender = data.get("gender")
        age = data.get("age")
        address = data.get("address")

        if User.find_user(email):
            return jsonify({"message": "User already exists !!"}), 404
        
        # if is_valid_user(user_id=user_id) == False:
        #     return jsonify({"message":"Enter valid twitter Id"}), 404
        
        User.create_user(name,email,password,gender,age,address)
        return jsonify({"message":"User Created successfully"}), 200
    except Exception as e:
        print(str(e))
        return jsonify({"message":"error occured in user creattion","error":str(e)}), 500
    

def log_in():
    try:    
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        if not User.find_user(email):
            return jsonify({"message":"User not registered first signup"}), 400
        if not User.verify_user(email,password):
            return jsonify({"message":"password wrong"}), 404
        
        # Generate JWT token
        payload = {
            "email": email,
            "exp": datetime.utcnow() + timedelta(hours=1)  # Token valid for 1 hour
        }
        token = jwt.encode(payload, os.getenv('JWT_SECRET'), algorithm="HS256")

        return jsonify({"message": "User logged in successfully", "token": token}), 200
        # return jsonify({"message":"User logged in successfully"}),200
    except Exception as e:
        print(str(e))
        return jsonify({"message":"error occured","error":str(e)}), 500
    
# def verify_user():
#     try:
#         data = request.get_json()
#         user_id = data.get("user_id")
#         otp = data.get("otp")



def retrive_data():
    try:
        data = request.get_json()
        email = data.get('email')

        if not email:
            jsonify({"message":"Email is neccessary"}), 400
        
        user = User.find_user(email)

        if user:
            user_data = {
                "name" : user["name"],
                "email" : user["email"],
                "user_id" : user["user_id"],
                "gender" : user["gender"],
                "age" : user["age"],
                "address" : user["address"],
                "image_url" : user["image_url"]
            }
        
        return jsonify({"message":"user retrieved succussfully","user":user_data}), 200
    except Exception as e:
        print(str(e))
        return jsonify({"message": "error occured","error":str(e)}),500
 
def update_twitter_username():
    try:
        data = request.get_json()
        email = data.get("email")
        user_id = data.get("user_id")

        if not email:
            return jsonify({"message":"provide the email"}), 404
        
        if not user_id:
            return jsonify({"message":"provide the twitter username"}), 404
        
        user = User.find_user(email)

        if not user:
            return jsonify({"message":"User not found"}), 400
        
        User.update_user_twitter_username(email, user_id)
        return jsonify({"success":True,"message":"User updated"}),200
    except Exception as e:
        print(str(e))
        return jsonify({"error":f"error in updation of user {str(e)}"}), 500

def handle_form_submit():
    try:
        data = request.get_json()
        email = data.get('email')
        q1 = data.get('q1')
        q2 = data.get('q2')
        q3 = data.get('q3')
        q4 = data.get('q4')
        q5 = data.get('q5')
        q6 = data.get('q6')
        q7 = data.get('q7')
        q8 = data.get('q8')
        q9 = data.get('q9')

        sum_of_ans = q1+q2+q3+q4+q5+q6+q7+q8+q9
        # Set currentmh based on the value of sum_of_ans
        if 1 <= sum_of_ans <= 4:
            currentmh = 0.87
        elif 5 <= sum_of_ans <= 9:
            currentmh = 0.62
        elif 10 <= sum_of_ans <= 14:
            currentmh = 0
        elif 15 <= sum_of_ans <= 19:
            currentmh = -0.62
        elif 20 <= sum_of_ans <= 27:
            currentmh = -0.87
        else:
            # Handle other cases as needed
            currentmh = 0.9
        
        user = User.find_user(email)
        username = user['user_id'] # retrieving user's twitter username
        rest_id = user['rest_id'] # retrieving user's twitter rest id

        folderpath = f"dataset/{username}"
        filename = f"all_sentiment_score_{rest_id}.csv"
        filepath = os.path.join(folderpath,filename)
        df = pd.read_csv(filepath)

        twitter_score = df['average_sentiment_score'].iloc[0]
        # Assign weights (70% for form score, 30% for Twitter score)
        weight_form = 0.7
        weight_twitter = 0.3

        # Calculate weighted mental health score
        mental_health_score = (currentmh * weight_form) + (twitter_score * weight_twitter)

        updated_user = User.update_user_score(email,mental_health_score)
        if updated_user:
            print(f"{username} mental health score updated in mongo")
        else:
            print(f"error is updating score of {username}")
        
        return jsonify({"success":True, "Score" : mental_health_score}), 200
    except Exception as e:
        print(str(e))
        return jsonify({"success":False,"error":str(e)}), 500
    

def convert_to_percentage(value, max_range,min_range):
    
    # Convert the value to percentage scale
    percentage = abs(round(((value - min_range) / (max_range - min_range)) * 100, 2))

    percentage = max(min(percentage, 100), 0)
    return percentage

def result():
    try:
        data = request.get_json()
        email = data.get('email')

        user = User.find_user(email)
        score = user['mental_health_score']
        result = convert_to_percentage(score,1,-1)
        print(result)
        return jsonify({"success" : True, "result" : result}), 200
    except Exception as e:
        print(str(e))
        return jsonify({"success" : False, "error" : str(e)}), 500

def graph():
    try:
        data = request.get_json()
        email = data.get('email')

        user = User.find_user(email)
        user_id = user['user_id']
        rest_id = user['rest_id']
        result = user['mental_health_score']

        mscore = convert_to_percentage(result,1,-1)
        print(mscore)

        folderpath = f"dataset/{user_id}"
        filename = f"analyzedDataFinalProduct_{rest_id}.csv"
        filepath = os.path.join(folderpath,filename)
        df = pd.read_csv(filepath)
        # print(df)

        datelist = []

        scorelist = []

        num = len(df)

        if num > 10:
            interval = num // 10
            df=df.iloc[::interval][:10]
        
        for score,date in zip(df['sentiment_score'], df['created_at']):
            datelist.append(date)
            percen_score = convert_to_percentage(score,1,-1)
            scorelist.append(percen_score)
        
        # Add the current date and user's latest mental health score
        current_date = datetime.now().strftime('%d %b %y')  # Format: '13 Aug 23'
        datelist.append(current_date)
        scorelist.append(mscore)
        
        if not datelist or not scorelist:
            return jsonify({"success":False, "message":"no data is provided"}),404

        return jsonify({"success" : True, "dates":datelist, "scores" : scorelist}),200
        # return jsonify({
        #     "success":True,
        #     "data" : {
        #         "date" : datelist,
        #         "score" : scorelist
        #     } 
        # }),200

    except Exception as e:
        print(str(e))
        return jsonify({"success":False,"error":str(e)}),500