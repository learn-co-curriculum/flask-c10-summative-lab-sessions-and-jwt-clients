#!/usr/bin/env python3
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