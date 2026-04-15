from faker import Faker
from flask import Flask
from flask_bcrypt import Bcrypt

from app import create_app
from models import db, User, Note

fake = Faker()
app = create_app()
bcrypt = Bcrypt(app)

with app.app_context():
    db.drop_all()
    db.create_all()

    admin = User(
        username="demo",
        password_digest=bcrypt.generate_password_hash("password").decode("utf-8"),
    )
    db.session.add(admin)
    db.session.commit()

    notes = []
    for _ in range(12):
        notes.append(
            Note(
                title=fake.sentence(nb_words=5),
                content=fake.paragraph(nb_sentences=3),
                mood=fake.word(ext_word_list=["productive", "lazy", "focused", "rested"]),
                user_id=admin.id,
            )
        )
    db.session.add_all(notes)
    db.session.commit()

    print("Seed data created:")
    print(f"- user demo / password password")
    print(f"- {len(notes)} notes")
