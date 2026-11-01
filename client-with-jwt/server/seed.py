from faker import Faker
from server import create_app, db
from server.models import User, Recipe

app = create_app()
fake = Faker()

with app.app_context():
    print("Clearing old data...")
    Recipe.query.delete()
    User.query.delete()

    print("Seeding demo user...")
    chef = User(username="joseph_chef")
    chef.password = "password123"
    db.session.add(chef)
    db.session.commit()