
from app import app
from models import db, User, Task

with app.app_context():
    user = User.query.filter_by(username="demo").first()

    if not user:
        user = User(username="demo")
        user.set_password("demo1234")
        db.session.add(user)
        db.session.commit()

    if not Task.query.filter_by(user_id=user.id).first():
        tasks = [
            Task(title="Study Flask", description="Revise Flask routes", user_id=user.id),
            Task(title="Finish project", description="Complete backend lab", user_id=user.id),
            Task(title="Test API", description="Check all endpoints", user_id=user.id),
            Task(title="Update GitHub", description="Push project changes", user_id=user.id),
            Task(title="Write README", description="Document the project", user_id=user.id),
            Task(title="Review code", description="Check for errors", user_id=user.id)
        ]

        db.session.add_all(tasks)
        db.session.commit()

    print("Database seeded successfully!")
