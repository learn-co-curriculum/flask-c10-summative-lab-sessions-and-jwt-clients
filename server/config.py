import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
class Config:

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")

class DevelopmentConfig(Config):
    debug = True
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(BASE_DIR, 'instance', 'app.db')}'

config_by_name = {
    'development' : DevelopmentConfig
}