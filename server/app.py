from flask import Flask
from config import Config
from models import db, bcrypt
from flask_migrate import Migrate
from routes.auth import auth_bp
from routes.notes import notes_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    Migrate(app, db)

    app.register_blueprint(auth_bp)
    app.register_blueprint(notes_bp)

    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Origin", "http://localhost:3000")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
        response.headers.add("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,PATCH,OPTIONS")
        response.headers.add("Access-Control-Allow-Credentials", "true")
        return response

    @app.route("/")
    def index():
        return {"message": "Notes API"}, 200

    return app


app = create_app()

if __name__ == "__main__":
    app.run(port=5555, debug=True)