from app import app
from config import db
from models import User, Note


def seed_data():
    with app.app_context():

        # Sample users
        users_data = [
            {
                "username": "john",
                "password": "password123"
            },
            {
                "username": "mary",
                "password": "password456"
            }
        ]

        users = {}

        # Create users if they don't already exist
        for user_data in users_data:
            user = User.query.filter_by(
                username=user_data["username"]
            ).first()

            if not user:
                user = User(username=user_data["username"])
                user.set_password(user_data["password"])
                db.session.add(user)
                db.session.flush()

            users[user.username] = user

        # Sample notes
        notes_data = [
            {
                "title": "My First Note",
                "content": "This is John's first sample note.",
                "username": "john"
            },
            {
                "title": "Learning Flask",
                "content": "I am learning how to build APIs with Flask.",
                "username": "john"
            },
            {
                "title": "My Daily Tasks",
                "content": "Complete assignments and practise coding.",
                "username": "mary"
            },
            {
                "title": "Project Ideas",
                "content": "Build useful applications using Python.",
                "username": "mary"
            }
        ]

        # Create notes without duplicating existing ones
        for note_data in notes_data:
            user = users[note_data["username"]]

            existing_note = Note.query.filter_by(
                title=note_data["title"],
                user_id=user.id
            ).first()

            if not existing_note:
                note = Note(
                    title=note_data["title"],
                    content=note_data["content"],
                    user_id=user.id
                )
                db.session.add(note)

        db.session.commit()

        print("Sample users and notes seeded successfully!")


if __name__ == "__main__":
    seed_data()
