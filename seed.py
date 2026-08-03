from app import create_app
from extensions import db
from models import Note, User


app = create_app()

with app.app_context():
    # The schema is managed by Flask-Migrate; this only resets starter data.
    Note.query.delete()
    User.query.delete()
    db.session.commit()

    dale = User(username="Dale")
    dale.password = "securepass123"
    grace = User(username="")
    grace.password = "securepass123"
    db.session.add_all([dale, grace])
    db.session.flush()
    db.session.add_all([
        Note(title="Launch checklist", content="Review API routes and deployment settings.", user_id=dale.id),
        Note(title="Weekly reflection", content="Document lessons from the sprint.", user_id=dale.id),
        Note(title="Research ideas", content="Read about database indexing.", user_id=grace.id),
    ])
    db.session.commit()
    print("Seeded users and notes.")
