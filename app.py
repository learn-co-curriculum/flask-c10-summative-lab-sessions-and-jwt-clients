from flask import Flask, jsonify

from config import Config
from extensions import bcrypt, db, migrate
from routes import api


def create_app(config_object=Config):
    app = Flask(__name__)
    app.config.from_object(config_object)
    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    app.register_blueprint(api)

    @app.get("/")
    def index():
        return jsonify({"message": "Notes API is running."})

    @app.errorhandler(404)
    def not_found(_error):
        return jsonify({"error": "Route not found."}), 404

    return app


app = create_app()


if __name__ == "__main__":
    app.run(port=5555, debug=True)
