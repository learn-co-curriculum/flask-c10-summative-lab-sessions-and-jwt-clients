from app import create_app
from models import User, Note, db
from faker import Faker

app = create_app()

with app.app_context():
    db.create_all()

    fake = Faker()

    users = []
    for _ in range(5):
        username = fake.user_name()
        user = User(username=username)
        user.password_hash = 'password'
        users.append(user)
        db.session.add(user)

    db.session.commit()

    print("Seeded database with users")

    print("Seeded database with users and notes")