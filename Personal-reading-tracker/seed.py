from datetime import date

from flask_bcrypt import generate_password_hash

from app import app
from models import db, User, ReadingEntry

with app.app_context():

    print('Clearing existing data...')
    ReadingEntry.query.delete()
    User.query.delete()

    print('Seeding users...')
    user1 = User(
        username='jamesk',
        email='jamesk@example.com',
        password_hash=generate_password_hash('password123').decode('utf-8')
    )
    user2 = User(
        username='aisha_m',
        email='aisha_m@example.com',
        password_hash=generate_password_hash('password123').decode('utf-8')
    )

    db.session.add_all([user1, user2])
    db.session.commit()

    print('Seeding reading entries...')
    entries = [
        ReadingEntry(
            title='Atomic Habits',
            author='James Clear',
            status='completed',
            rating=5,
            start_date=date(2024, 1, 3),
            completion_date=date(2024, 1, 20),
            user=user1
        ),
        ReadingEntry(
            title='Dune',
            author='Frank Herbert',
            status='reading',
            rating=None,
            start_date=date(2024, 3, 1),
            completion_date=None,
            user=user1
        ),
        ReadingEntry(
            title='Deep Work',
            author='Cal Newport',
            status='want_to_read',
            rating=None,
            start_date=None,
            completion_date=None,
            user=user2
        ),
        ReadingEntry(
            title='Project Hail Mary',
            author='Andy Weir',
            status='completed',
            rating=4,
            start_date=date(2024, 2, 10),
            completion_date=date(2024, 2, 28),
            user=user2
        ),
    ]

    db.session.add_all(entries)
    db.session.commit()

    print('Done seeding!')