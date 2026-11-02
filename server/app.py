from flask import Flask, jsonify
from config import db, migrate, bcrypt

app = Flask(__name__)

# Application configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "development-key-change-later"

# Connect Flask to our shared tools
db.init_app(app)
migrate.init_app(app, db)
bcrypt.init_app(app)

# Import database models
import models


@app.route("/")
def home():
    return jsonify({"message": "Personal Notes API is running"}), 200


if __name__ == "__main__":
    app.run(port=5555, debug=True)