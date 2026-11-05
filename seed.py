"""Seed the database with demo users and notes.

Usage: python seed.py   (run `flask db upgrade` first)
Every demo user has the password "password123".
"""
from faker import Faker

from app import app
from config import db
from models import Note, User

fake = Faker()

DEMO_USERNAMES = ["alice", "bob", "charlie"]
DEMO_PASSWORD = "password123"
CATEGORIES = ["work", "personal", "ideas", "shopping", "study"]
NOTES_PER_USER = 15  # more than one page, so pagination is easy to demo


def seed():
    with app.app_context():
        print("Clearing old data...")
        Note.query.delete()
        User.query.delete()
        db.session.commit()

        print("Creating users and notes...")
        for username in DEMO_USERNAMES:
            user = User(username=username)
            user.password_hash = DEMO_PASSWORD
            db.session.add(user)
            db.session.flush()  # assigns user.id

            for _ in range(NOTES_PER_USER):
                db.session.add(
                    Note(
                        title=fake.sentence(nb_words=4).rstrip("."),
                        content=fake.paragraph(nb_sentences=3),
                        category=fake.random_element(CATEGORIES),
                        is_pinned=fake.boolean(chance_of_getting_true=15),
                        user_id=user.id,
                    )
                )

        db.session.commit()
        print(f"Seeded {len(DEMO_USERNAMES)} users with {NOTES_PER_USER} notes each.")
        print(f'Log in as any of {DEMO_USERNAMES} with password "{DEMO_PASSWORD}".')


if __name__ == "__main__":
    seed()