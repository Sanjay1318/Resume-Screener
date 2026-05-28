import os
from dotenv import load_dotenv

# Load the hidden variables from the .env file
load_dotenv()

class Config:
    # Safely pulling keys from the environment!
    SECRET_KEY = os.environ.get('SECRET_KEY')
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
    
    # Keep your database and upload folder configs the same
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost/resume_scanner'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'resume_uploads'