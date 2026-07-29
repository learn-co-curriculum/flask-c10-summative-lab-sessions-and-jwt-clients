from app import app
from models import Note, User, db


SEED_USERS = [
    {
        "username": "alice",
        "email": "alice@example.com",
        "password": "password123",
        "notes": [
            ("Welcome", "This is Alice's first note."),
            ("Shopping", "Coffee, bread, and fruit."),
            ("Project ideas", "Build a notes API with Flask."),
        ],
    },
    {
        "username": "bob",
        "email": "bob@example.com",
        "password": "password123",
        "notes": [
            ("Meeting", "Review the API endpoints tomorrow."),
            ("Reading list", "Flask documentation and SQLAlchemy guides."),
            ("Weekend", "Go hiking if the weather is clear."),
        ],
    },
]


def seed():
    for data in SEED_USERS:
        user = User.query.filter_by(username=data["username"]).first()
        if user:
            continue
        user = User(username=data["username"], email=data["email"])
        user.set_password(data["password"])
        db.session.add(user)
        db.session.flush()
        db.session.add_all(
            [Note(title=title, content=content, user_id=user.id) for title, content in data["notes"]]
        )
    db.session.commit()


if __name__ == "__main__":
    with app.app_context():
        seed()
        print("Seed data created (or already present).")
