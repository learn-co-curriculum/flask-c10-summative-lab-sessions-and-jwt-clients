import os
class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL' , 'sqlite:///app.db')
    if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)

    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = "super-secret_key_here"  
    SECRET_KEY = "dev-secret_key_here"