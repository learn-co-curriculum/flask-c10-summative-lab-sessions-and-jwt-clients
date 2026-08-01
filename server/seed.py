#!/usr/bin/env python3
"""
seed.py
-------
Populates the database with sample data for development and testing.

Matches the User model which no longer has an email field, consistent
with what the client-with-sessions frontend sends during signup.

Seeded data:
    - 3 User accounts  (password: password123)
    - 5 Notes per user (15 notes total)

Safe to re-run — clears all existing records before inserting new ones.
"""

from faker import Faker

from config import app, db
from models import User, Note

fake = Faker()


def clear_data():
    """Delete all existing records from every table."""
    print("Clearing existing data...")
    Note.query.delete()
    User.query.delete()
    db.session.commit()
    print("  Done.")


def seed_users():
    """
    Create 3 sample user accounts with hashed passwords.
    All use the same password for easy manual testing.
    Returns the list of created User objects.
    """
    print("Seeding users...")
    users = []

    for _ in range(3):
        user = User(username=fake.unique.user_name())
        # password_hash setter hashes this automatically via bcrypt
        user.password_hash = 'password123'
        db.session.add(user)
        users.append(user)

    db.session.commit()
    print(f"  Created {len(users)} users.")
    return users


def seed_notes(users):
    """
    Create 5 notes for each user with randomly generated content.
    Each note is linked to its owner via user_id.
    """
    print("Seeding notes...")
    total = 0

    for user in users:
        for _ in range(5):
            note = Note(
                title   = fake.sentence(nb_words=5).rstrip('.'),
                content = fake.paragraph(nb_sentences=4),
                user_id = user.id,
            )
            db.session.add(note)
            total += 1

    db.session.commit()
    print(f"  Created {total} notes.")


def print_summary(users):
    """Print login credentials for all seeded accounts."""
    print("\n" + "=" * 45)
    print("Seed complete. Test accounts (password: password123):")
    print("=" * 45)
    for user in users:
        print(f"  id={user.id}  username={user.username}")
    print("=" * 45 + "\n")


def seed():
    with app.app_context():
        clear_data()
        users = seed_users()
        seed_notes(users)
        print_summary(users)


if __name__ == '__main__':
    seed()