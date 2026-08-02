from app import app
from config import db
from models import User, Task

with app.app_context():

    print("Deleting old data...")

    Task.query.delete()
    User.query.delete()

    print("Creating users...")

    user1 = User(
        username="emmanuel",
        email="emmanuel@gmail.com"
    )
    user1.password = "123456"

    user2 = User(
        username="john",
        email="john@gmail.com"
    )
    user2.password = "password"

    db.session.add_all([user1, user2])
    db.session.commit()

    print("Creating tasks...")

    task1 = Task(
        title="Complete Flask Lab",
        description="Finish backend API",
        status="Pending",
        user_id=user1.id
    )

    task2 = Task(
        title="Study JWT",
        description="Understand authentication",
        status="Completed",
        user_id=user1.id
    )

    task3 = Task(
        title="Workout",
        description="Go to the gym",
        status="Pending",
        user_id=user2.id
    )

    db.session.add_all([
        task1,
        task2,
        task3
    ])

    db.session.commit()

    print("Database seeded successfully!")