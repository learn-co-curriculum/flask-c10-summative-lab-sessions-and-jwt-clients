import os 
from dotenv import load_dotenv

load_dotenv()   
class Config():
    SECRET_KEY = os.environ.get("SECRET_KEY", "default_secret_key")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "default_jwt_secret")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False