from flask import Blueprint, request, jsonify
from controllers.user_controllers import sign_up,log_in,retrive_data,handle_form_submit,update_twitter_username
from controllers.user_controllers import graph, result
from controllers.email_controllers import send_otp,verify_otp

#defining the blueprints to tell flask 
user_bp = Blueprint('user',__name__)

# Defining routes
user_bp.route('/sign-up', methods=['POST'])(sign_up)
user_bp.route('/log-in', methods=['POST'])(log_in)
user_bp.route('/details', methods=['POST'])(retrive_data)
user_bp.route('/send-otp',methods=['POST'])(send_otp)
user_bp.route('/verify-otp',methods=['POST'])(verify_otp)
user_bp.route('/add-twitter-username', methods=['PUT'])(update_twitter_username)

# calculating final score
user_bp.route('/form', methods=['POST'])(handle_form_submit)
user_bp.route('/graph', methods=['POST'])(graph)
user_bp.route('/result', methods=['POST'])(result)