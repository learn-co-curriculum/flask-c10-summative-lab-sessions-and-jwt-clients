from app import app, db
from models import Note, User


with app.app_context():
    db.drop_all()
    db.create_all()

    users = [
        User(username="alice"),
        User(username="bob"),
    ]
    users[0].password = "password123"
    users[1].password = "password123"

    db.session.add_all(users)
    db.session.commit()

    notes = [
        Note(title="Morning plan", content="Review tasks and priorities for the day and protect the first focus block.", category="Notes", user_id=users[0].id),
        Note(title="Workout", content="30 minutes of cardio, strength work, and a 10-minute stretch reset.", category="Workouts", user_id=users[0].id),
        Note(title="Focus tasks", content="Finalize the landing page styling, polish the board, and confirm all API routes are stable.", category="Tasks", user_id=users[0].id),
        Note(title="Journal reflection", content="A cleaner interface and clearer layout made the workday feel calmer and more intentional.", category="Journal", user_id=users[0].id),
        Note(title="Project notes", content="Review the user flow for signup and make sure the login experience remains smooth.", category="Notes", user_id=users[1].id),
        Note(title="Workout checklist", content="Mobility work, a light run, and a quick recovery stretch before bed.", category="Workouts", user_id=users[1].id),
        Note(title="Weekly goals", content="Ship the productivity dashboard polish, confirm the DB data flow, and QA the final layout.", category="Tasks", user_id=users[1].id),
        Note(title="Daily journal", content="The app is feeling much more polished; the contrast and hierarchy are significantly better today.", category="Journal", user_id=users[1].id),
    ]

    db.session.add_all(notes)
    db.session.commit()

    print("Database seeded with users and notes.")
