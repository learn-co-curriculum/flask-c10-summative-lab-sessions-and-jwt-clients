from flask_bcrypt  import Bcrypt
from flask import Flask, make_response, request, jsonify, json
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from models import db

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config['JWT_SECRET_KEY'] = 'fake_secret_key'
jwt = JWTManager(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
migrate = Migrate(app, db)
db.init_app(app)
