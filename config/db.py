from flask import jsonify
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import os

def get_db():
    try:
        # client = MongoClient(os.getenv("MONGO_URI"))
        client = MongoClient(os.getenv("MONGO_ATLAS_URI"))
        db = client.ManoVision
        print("Connected to database: ",client.HOST)
        return db
    except Exception as e:
        print(str(e))
        return jsonify({"message" : "Error in connecting the database", "error" : str(e)}), 500