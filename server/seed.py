from random import choice, randint, sample

from faker import Faker

from app import app
from config import db
from models import MOOD_CHOICES, Activity, Journal, Mood, User, mood_activities

fake = Faker()

ACTIVITY_NAMES = ["Exercise", "Reading", "Work", "Socialising", "Meditation", "Cooking", "Gaming", "Studying"]


def make_user(username, password):
    user = User(username=username)
    user.password_hash = password
    db.session.add(user)
    return user


with app.app_context():
    print("Clearing old data...")
    db.session.execute(mood_activities.delete())
    Mood.query.delete()
    Journal.query.delete()
    Activity.query.delete()
    User.query.delete()
    db.session.commit()

    print("Creating users...")
    users = [make_user("demo", "password123")]
    for _ in range(2):
        users.append(make_user(fake.unique.user_name(), "password123"))
    db.session.commit()

    print("Creating activities, moods and journal entries...")
    for user in users:
        activities = [Activity(name=name, user=user) for name in sample(ACTIVITY_NAMES, 5)]
        db.session.add_all(activities)

        for _ in range(15):
            mood = Mood(
                mood=choice(MOOD_CHOICES),
                intensity=randint(1, 10),
                note=fake.sentence(nb_words=10),
                created_at=fake.date_time_between(start_date="-30d", end_date="now"),
                user=user,
            )
            mood.activities = sample(activities, randint(1, 3))
            db.session.add(mood)

        for _ in range(8):
            db.session.add(Journal(
                title=fake.sentence(nb_words=4).rstrip("."),
                content=fake.paragraph(nb_sentences=4),
                created_at=fake.date_time_between(start_date="-30d", end_date="now"),
                user=user,
            ))
    db.session.commit()

    print("Done! Log in as demo / password123")