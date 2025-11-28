from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    @app.route('/')
    def index():
        return {"message": "Server and DB ready!"}, 200

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(port=5555, debug=True)
