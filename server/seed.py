#!/usr/bin/env python3
"""
seed.py
-------
Populates the database with sample data for development and manual testing.

Seeded data:
    - 3 User accounts (password: password123 for all)
    - 5 Notes per user (15 notes total)

Safe to re-run — clears all existing data before seeding.
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
    print("  All records deleted.")


def seed_users():
    """
    Create 3 sample user accounts.
    All accounts share the password 'password123' for easy testing.
    Returns the list of created User objects.
    """
    print("Seeding users...")
    users = []

    for _ in range(3):
        user = User(
            username=fake.unique.user_name(),
            email=fake.unique.email(),
        )
        # password_hash setter automatically hashes this value with bcrypt
        user.password_hash = 'password123'
        db.session.add(user)
        users.append(user)

    db.session.commit()
    print(f"  Created {len(users)} users.")
    return users


def seed_notes(users):
    """
    Create 5 notes for each user.
    Each note has a randomly generated title and content.
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


def print_seed_summary(users):
    """Print a summary of all seeded accounts to the terminal."""
    print("\n" + "=" * 50)
    print("Seed complete. Test accounts (password: password123):")
    print("=" * 50)
    for user in users:
        print(f"  id={user.id}  username={user.username}  email={user.email}")
    print("=" * 50 + "\n")


def seed():
    """Run the full seed process inside the Flask app context."""
    with app.app_context():
        clear_data()
        users = seed_users()
        seed_notes(users)
        print_seed_summary(users)


if __name__ == '__main__':
    seed()