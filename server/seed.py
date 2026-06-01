from app import app
from config import db
from models import User, Note

with app.app_context():

    print("Clearing existing data...")

    # Delete all existing records to start fresh
    Note.query.delete()
    User.query.delete()

    print("Creating users...")

    user1 = User(username="alice")
    user1.password_hash = "password123"

    user2 = User(username="bob")
    user2.password_hash = "password123"

    db.session.add_all([user1, user2])
    db.session.commit()

    print("Creating notes...")

    notes = [
        Note(title="Alice Note 1", content="Hello from Alice", category="work", user_id=user1.id),
        Note(title="Alice Note 2", content="Another note", category="personal", user_id=user1.id),
        Note(title="Bob Note 1", content="Bob's first note", category="work", user_id=user2.id),
        Note(title="Bob Note 2", content="Bob here again", category="ideas", user_id=user2.id),
    ]

    db.session.add_all(notes)
    db.session.commit()

    print("Seeding complete!")