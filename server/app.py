from flask import Flask
from flask_restful import Api

from config import Config, db, migrate, bcrypt, jwt

app = Flask(__name__)
app.config.from_object(Config)

# Initialize API
api = Api(app)

# Initialize extensions
db.init_app(app)
migrate.init_app(app, db)
bcrypt.init_app(app)
jwt.init_app(app)

# Import models so Flask-Migrate detects them
import models

# Import resources
from resources.auth import Signup, Login, Me

# Register routes
api.add_resource(Signup, "/signup")
api.add_resource(Login, "/login")
api.add_resource(Me, "/me")

@app.route("/")
def home():
    return {"message": "Task Tracker API is running"}


if __name__ == "__main__":
    app.run(debug=True)