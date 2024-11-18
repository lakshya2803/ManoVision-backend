from flask import jsonify, request, current_app
import random
from flask_mail import Message
import time

# for this functionality to run go the settings of google account of the sender account and turn on the 
# less secure app access option in security

def generate_otp():
    otp = ""
    for _ in range(6):
        otp += str(random.randint(0,9))
    return otp

otp_storage = {}

def send_email(email, otp):
    from app import mail #lazy import to prevent circular import
    msg = Message("Your OTP for Email Verification",sender=current_app.config["MAIL_USERNAME"],
                  recipients=[email])
    msg.body = f"Your OTP is {otp}. Please use this to verify your email address."
    print(current_app)
    try:
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def send_otp():
    data = request.get_json()
    email = data.get('user_id')
    
    # Generate OTP and save it with a timestamp
    otp = generate_otp()
    otp_storage[email] = {"otp": otp, "timestamp": time.time()}
    
    # Send OTP to user's email
    if send_email(email, otp):
        return jsonify({"success": True, "message": "OTP sent to your email."}), 200
    else:
        return jsonify({"success": False, "message": "Failed to send OTP."}), 500

def verify_otp():
    data = request.get_json()
    email = data.get('user_id')
    otp = data.get('otp')
    
    # Check if the OTP exists for the given email and is not expired
    if email in otp_storage:
        stored_otp = otp_storage[email]["otp"]
        timestamp = otp_storage[email]["timestamp"]
        
        # OTP is valid for 5 minutes (300 seconds)
        if time.time() - timestamp > 300:
            return jsonify({"success": False, "message": "OTP expired."})
        
        if otp == stored_otp:
            return jsonify({"success": True, "message": "Email verified successfully."})
        else:
            return jsonify({"success": False, "message": "Invalid OTP."})
        
    else:
        return jsonify({"success": False, "message": "OTP not found."})

