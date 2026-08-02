#!/usr/bin/env python3

from app import app
from models import db, User, Note

with app.app_context():

    
    Note.query.delete()
    User.query.delete()
    db.session.commit()

   
    user1 = User(username="karani")
    user1.password_hash = "password123"

    user2 = User(username="Elsie")
    user2.password_hash = "password456"

    db.session.add_all([user1, user2])
    db.session.commit()

    
    note1 = Note(title="Grocery list", content="Eggs, milk, bread", category="Personal", user=user1)
    note2 = Note(title="Project ideas", content="Build a notes app", category="Work", user=user1)
    note3 = Note(title="Workout plan", content="Push ups, running", category="Health", user=user2)

    db.session.add_all([note1, note2, note3])
    db.session.commit()

    print("yay, Database seeded successfully!, amazing")