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

    print("Seeding recipes...")
    for _ in range(12):
        recipe = Recipe(
            title=fake.word().capitalize() + " Delight",
            prep_time_minutes=fake.random_int(min=10, max=60),
            ingredients=", ".join([fake.word() for _ in range(4)]),
            is_favorite=fake.boolean(),
            user_id=chef.id
        )
        db.session.add(recipe)

    db.session.commit()
    print("Database seeding completed!")