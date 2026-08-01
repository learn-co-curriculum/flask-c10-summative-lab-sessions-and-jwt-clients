from flask import Flask
from config import Config, db, migrate, bcrypt, jwt

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
migrate.init_app(app, db)
bcrypt.init_app(app)
jwt.init_app(app)

# Import models so Flask-Migrate can detect them
import models


@app.route("/")
def home():
    return {"message": "Task Tracker API is running"}


if __name__ == "__main__":
    app.run(debug=True)