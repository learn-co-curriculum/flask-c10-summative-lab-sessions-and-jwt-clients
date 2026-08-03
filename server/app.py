from flask import Flask, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from schemas import user_schema

from config import Config, db, bcrypt, migrate, jwt

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
bcrypt.init_app(app)
migrate.init_app(app, db)
jwt.init_app(app)

from models import User, Task


@app.route("/")
def home():
    return {"message": "Productivity API is running!"}

@app.post("/signup")
def signup():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")
    password_confirmation = data.get("password_confirmation")

    if password != password_confirmation:
        return {"errors": ["passwords do not match, try again"]}, 400

    existing_user = User.query.filter_by(username=username).first()

    if existing_user:
        return {"errors": ["Username already exists."]}, 400

    try:
        user = User(username=username)
        user.password = password

        db.session.add(user)
        db.session.commit()
    except ValueError as e:
        return {"errors": [str(e)]}, 400

    token = create_access_token(identity=str(user.id))

    return{
        "token" : token,
        "user" : user_schema.dump(user)
    }, 201

@app.post("/login")
def login():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()

    if not user or not user.authenticate(password):
        return {"errors": ["Invalid username or password."]}, 401

    token = create_access_token(identity=str(user.id))

    return {
        "token": token,
        "user": user_schema.dump(user)
    }, 200 

@app.get("/me")
@jwt_required()
def me():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)

    if not user:
        return{"errors": ["User not found."]}, 404

    return user_schema.dump(user), 200
    


if __name__ == "__main__":
    app.run(port=5555, debug=True)