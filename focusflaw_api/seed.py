from app import app
from extensions import db
from models import User, Task


with app.app_context():


    Task.query.delete()
    User.query.delete()


    user1 = User(
        username="Ryan",
        email="ryan@example.com"
    )
    user1.set_password("12345")

    user2 = User(
        username="Alice",
        email="alice@example.com"
    )
    user2.set_password("67890")

    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()


    tasks = [
        Task(
            title="Finish Flask Summative",
            description="Complete the backend project.",
            completed=False,
            user_id=user1.id
        ),
        Task(
            title="Revise Module 5",
            description="Review Marshmallow and Sessions.",
            completed=False,
            user_id=user1.id
        ),
        Task(
            title="Push Project to GitHub",
            description="Commit and push the final code.",
            completed=True,
            user_id=user1.id
        ),
        Task(
            title="Read Documentation",
            description="Study Flask documentation.",
            completed=False,
            user_id=user2.id
        )
    ]

    db.session.add_all(tasks)
    db.session.commit()

    print("Database successfully seeded!")
