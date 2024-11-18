from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os
from config.db import get_db

# importing modules for email functionality
from flask_mail import Mail


load_dotenv('config/config.env')
load_dotenv()
app = Flask(__name__)
CORS(app)

# Set up MongoDB URI, Secret Key, and Port directly from environment variables
# app.config['MONGODB_URI'] = os.getenv("MONGODB_URI")
app.config['MONGODB_URI'] = os.getenv("MONGO_ATLAS_URI2")
# app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

# connecting to the mongodb 
get_db()

# donot use this from college wifi as it is blocked in that
# setting up flask mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587 #for tls if used ssl then it should be 465
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv("MY_EMAIL")
app.config['MAIL_PASSWORD'] = os.getenv("EMAIL_PASS")  # Better to use environment variables here
app.config['MAIL_DEFAULT_SENDER'] = os.getenv("DEFAULT_SENDER")
mail = Mail(app)

# app.config.update(
#     MAIL_SERVER = 'smtp.gmail.com',
#     MAIL_PORT = 465,
#     MAIL_USERNAME = os.getenv("MY_EMAIL"),
#     MAIL_PASSWORD = os.getenv("EMAIL_PASS"),
#     MAIL_DEFAULT_SENDER = os.getenv("DEFAULT_SENDER")
# )

#register the blueprints to distinct between files where to go
from routes.user_routes import user_bp
from routes.twiitter_routes import twitter_bp
app.register_blueprint(user_bp, url_prefix='/api/v1/user')
app.register_blueprint(twitter_bp, url_prefix='/api/v1/twitter')

if __name__ == '__main__':
    port = int(os.getenv("PORT",5000))
    hostname = str(os.getenv("hostname",'0.0.0.0'))
    app.run(host=hostname,port=port,debug=True)