from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_restful import Api

from models import db
from resources.config import Config
from resources.auth import SignupResource, LoginResource, MeResource
from resources.notes import NotesResource, NoteResource

def create_app():
    """Create and configure the Flask app"""
    # Create Flask app
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    Bcrypt(app)
    JWTManager(app)
    Migrate(app, db)

    # Set up API routes
    api = Api(app)
    api.add_resource(SignupResource, '/signup')
    api.add_resource(LoginResource, '/login')
    api.add_resource(MeResource, '/me')
    api.add_resource(NotesResource, '/notes')
    api.add_resource(NoteResource, '/notes/<int:note_id>')

    @app.route('/')
    def home():
        """Home route for the API"""
        return {"message": "Welcome to the Productivity App API. See README for endpoints."}, 200

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)