"""Entry point: registers all routes.

Run with `flask run -p 5555` or `python app.py` (the React client's proxy
points at port 5555).
"""
from config import api, app
import models  # noqa: F401  (ensures models are registered for migrations)
from resources.auth import CheckSession, Login, Logout, Signup
from resources.notes import NoteDetail, NoteList

api.add_resource(Signup, "/signup")
api.add_resource(Login, "/login")
api.add_resource(Logout, "/logout")
api.add_resource(CheckSession, "/check_session")
api.add_resource(NoteList, "/notes")
api.add_resource(NoteDetail, "/notes/<int:note_id>")

if __name__ == "__main__":
    app.run(port=5555, debug=True)