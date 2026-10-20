from faker import Faker
from random import randint

from config import app, db
from models import User, Note

fake = Faker()

with app.app_context():
    print("Clearing old data...")
    Note.query.delete()
    User.query.delete()
    db.session.commit()

    print("Seeding users...")
    users = []
    for name in ["alice", "bob", "carol"]:
        user = User(username=name)
        user.password_hash = "password123"
        users.append(user)
    db.session.add_all(users)
    db.session.commit()

    print("Seeding notes...")
    for user in users:
        for _ in range(randint(8, 12)):
            db.session.add(Note(
                title=fake.sentence(nb_words=4),
                content=fake.paragraph(nb_sentences=3),
                user_id=user.id,
            ))
    db.session.commit()
    print("Done! Log in as alice, bob, or carol with password: password123")