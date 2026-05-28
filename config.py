import os
from dotenv import load_dotenv

# Load the hidden environment variables from your .env file
load_dotenv()

class Config:
    # Existing App Security & Database Settings
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'resume_uploads')
    MAX_CONTENT_LENGTH = 20 * 1024 * 1024  # 20MB limit
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

    # Flask-Mail SMTP Configuration for Gmail
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    
    # Securely pulling your email credentials from the .env file
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    
    # Sets your new email as the default sender for all OTPs
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_USERNAME')