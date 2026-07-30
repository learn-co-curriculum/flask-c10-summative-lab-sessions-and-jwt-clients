from faker import Faker
import random
from datetime import datetime

from config import app, db
from models import User, Workout

fake = Faker()
with app.app_context():
    print("Clearing database...")

    Workout.query.delete()
    User.query.delete()

    print("Creating users...")

    alice = User(username="alice")
    alice.password_hash = "password123"

    bob = User(username="bob")
    bob.password_hash = "password123" 

    celline = User(username="celline")
    celline.password_hash = "password123"

    users = [alice, bob, celline]

    db.session.add_all(users)
    db.session.commit()

    print("Creating Workouts...")
    workout_titles = [
        "Leg Day",
        "Upper Body",
        "Cardio",
        "Yoga",
        "HIIT",
        "Core Strength",
        "Running",
        "Full Body",
        "Cycling",
        "Stretching"
    ]

    for user in users:
        for _ in range(5):
            workout = Workout(
                title=random.choice(workout_titles),
                duration=random.randint(20, 90),
                date=fake.date_between(start_date="-30d", end_date="today"),
                user_id=user.id
            )

            db.session.add(workout)

    db.session.commit()
    print ("Database seeded successfully!")