from config import api, app
from resources.activities import Activities, ActivityById, MoodActivityLink
from resources.auth import CheckSession, Login, Logout, Signup
from resources.journals import JournalById, Journals
from resources.moods import MoodById, Moods

api.add_resource(Signup, "/signup")
api.add_resource(Login, "/login")
api.add_resource(CheckSession, "/check_session")
api.add_resource(Logout, "/logout")

api.add_resource(Moods, "/moods")
api.add_resource(MoodById, "/moods/<int:id>")

api.add_resource(Journals, "/journals")
api.add_resource(JournalById, "/journals/<int:id>")

api.add_resource(Activities, "/activities")
api.add_resource(ActivityById, "/activities/<int:id>")
api.add_resource(MoodActivityLink, "/moods/<int:mood_id>/activities/<int:activity_id>")

if __name__ == "__main__":
    app.run(port=5555, debug=True)