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


# --- RECIPE CRUD & PAGINATION ---

@app.route('/recipes', methods=['GET', 'POST'])
def handle_recipes():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    if request.method == 'GET':
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 5, type=int)

        pagination = Recipe.query.filter_by(user_id=user_id).paginate(
            page=page, per_page=per_page, error_out=False
        )

        return jsonify({
            "recipes": [r.to_dict() for r in pagination.items],
            "total": pagination.total,
            "pages": pagination.pages,
            "current_page": pagination.page
        }), 200

    elif request.method == 'POST':
        data = request.get_json()
        try:
            new_recipe = Recipe(
                title=data.get('title'),
                instructions=data.get('instructions'),
                prep_time_minutes=data.get('prep_time_minutes', 15),
                ingredients=data.get('ingredients', ''),
                is_favorite=data.get('is_favorite', False),
                user_id=user_id
            )
            db.session.add(new_recipe)
            db.session.commit()
            return jsonify(new_recipe.to_dict()), 201
        except Exception as e:
            return jsonify({"error": "Invalid recipe data"}), 400