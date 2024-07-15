# app/config.py

import os

class Config:
    SQLALCHEMY_DATABASE_URI =  os.getenv('DATABASE_URL') 
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')  # Ensure OPENAI_API_KEY is set in your environment variables
    

