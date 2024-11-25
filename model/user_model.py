from config.db import get_db

class User:
    def __init__(self,name,email,user_id,password,gender,age,address,mental_health_score, rest_id, image_url,twiiter_score):    #changed here
        self.name = name
        self.email = email
        self.user_id = user_id
        self.password = password
        self.gender = gender
        self.age = age
        self.address = address
        self.mental_health_score = mental_health_score
        self.rest_id = rest_id
        self.image_url = image_url
        self.twitter_score = twiiter_score #changed here
        
    @staticmethod
    def create_user(name,email,password,gender,age,address):
        db = get_db()
        user_data = {
            "name" : name,
            "email" : email,
            "password" : password,
            "gender" : gender,
            "age" : age,
            "address" : address
        }
        db.users.insert_one(user_data)
    
    @staticmethod
    def find_user(email):
        db = get_db()
        return db.users.find_one({"email":email})

    @staticmethod
    def verify_user(email,password):
        user = User.find_user(email)
        if user and user['password'] == password:
            return True
        else:
            return False

    @staticmethod       # new method
    def add_twitter_score(email,twitter_score):
        db = get_db()
        result = db.users.update_one(
            {"email" : email},
            {"$set" : {"twitter_score" : twitter_score}}
        )
        return result.modified_count > 0;

    @staticmethod
    def update_user_twitter_username(email,user_id):
        db = get_db()
        update_data = {
            "user_id" : user_id
        }
        result = db.users.update_one(
            {"email": email}, 
            {"$set": update_data}
        )
        return result.modified_count > 0  # Return True if an update occurred


    @staticmethod
    def update_user_twitter_info(email, rest_id, image_url):
        db = get_db()
        update_data = {
            "rest_id": rest_id,
            "image_url": image_url
        }
        result = db.users.update_one(
            {"email": email}, 
            {"$set": update_data}
        )
        return result.modified_count > 0  # Return True if an update occurred
    
    @staticmethod
    def update_user_score(email,mental_health_score):
        db = get_db()
        result = db.users.update_one(
            {"email": email}, 
            {"$set": {"mental_health_score" : mental_health_score}}
        )
        return result.modified_count > 0  # Return True if an update occurred
    
