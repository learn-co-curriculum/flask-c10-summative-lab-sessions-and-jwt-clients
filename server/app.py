from config import create_app, db
from flask_restful import Api
from models import User, Note
from resources.auth import Register, Login, Logout, CheckSession
from resources.notes import NoteList, NoteDetail

# Create the Flask app
app = create_app()

# Initialize Api directly with app
api = Api(app)

# Register auth routes
api.add_resource(Register, '/register')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(CheckSession, '/check_session')

# Register notes routes
api.add_resource(NoteList, '/notes')
api.add_resource(NoteDetail, '/notes/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)