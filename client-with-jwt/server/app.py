from flask import Flask, request, session, jsonify
from flask_bcrypt import Bcrypt
from server.models import db, User, Recipe


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipe_planner.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'super_secret_key_change_me'

db.init_app(app)
bcrypt = Bcrypt(app)


@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Recipe Planner API!"})



@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), 422

    try:
        user = User(username=username)
        user.password = password
        db.session.add(user)
        db.session.commit()

        session['user_id'] = user.id
        return jsonify(user.to_dict()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data.get('username')).first()

    if user and user.authenticate(data.get('password')):
        session['user_id'] = user.id
        return jsonify(user.to_dict()), 200

    return jsonify({"error": "Invalid username or password"}), 401


@app.route('/check_session', methods=['GET'])
def check_session():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.get(user_id)
        if user:
            return jsonify(user.to_dict()), 200
    return jsonify({"error": "Unauthorized"}), 401


@app.route('/logout', methods=['DELETE'])
def logout():
    if session.get('user_id'):
        session.pop('user_id', None)
        return {}, 204
    return jsonify({"error": "Unauthorized"}), 401