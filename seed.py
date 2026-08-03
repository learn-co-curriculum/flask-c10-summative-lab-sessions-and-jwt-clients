from app import app
from models import db, User, Note


with app.app_context():
    db.drop_all()
    db.create_all()

    user = User(username="demo", password="password123")
    db.session.add(user)
    db.session.commit()

    notes = [
        Note(title="Plan for today", content="Finish the lab and test the endpoints.", user_id=user.id),
        Note(title="Quick reminder", content="Double check the auth flow before submission.", user_id=user.id),
    ]

    db.session.add_all(notes)
    db.session.commit()

    print("Seeded demo user and sample notes.")
