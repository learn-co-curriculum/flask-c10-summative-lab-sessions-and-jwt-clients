"""Seed the database with sample data"""
from app import create_app
from models import User, Note, db
from faker import Faker

# Create app
app = create_app()

with app.app_context():
    # Create tables
    db.create_all()

    fake = Faker()

    # Create some users
    users = []
    for _ in range(5):
        username = fake.user_name()
        user = User(username=username)
        user.password_hash = 'password'  # simple password for seeding
        users.append(user)
        db.session.add(user)

    db.session.commit()

    # Create notes for each user
    for user in users:
        for _ in range(3):
            note = Note(
                title=fake.sentence(),
                content=fake.text(),
                user_id=user.id
            )
            db.session.add(note)

    db.session.commit()

    print("Seeded database with users and notes")