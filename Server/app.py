from flask import Flask, session
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_restful import Api

from models import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '1234'
app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.config['SESSION_COOKIE_SECURE'] = False

db.init_app(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
api = Api(app)

from resources import *

register_routes(api)

if __name__ == '__main__':
    app.run(debug=True, port=5555)