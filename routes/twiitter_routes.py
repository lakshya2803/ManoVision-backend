from flask import Blueprint
# from chatbot.twitter import tweet_extraction
from chatbot.get_user_info import get_user_info_api
from chatbot.talk import chatbot

twitter_bp = Blueprint('twitter',__name__)

twitter_bp.route('/userapi_info',methods=['POST'])(get_user_info_api)

# chatbot routes 
twitter_bp.route('/chatbot', methods=['POST'])(chatbot)