import os
class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL' , 'sqlite:///app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = "super-secret_key_here"  
    SECRET_KEY = "dev-secret_key_here"