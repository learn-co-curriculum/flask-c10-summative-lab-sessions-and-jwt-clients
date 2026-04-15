from app import app
from models import db, User, Expense
from faker import Faker

fake = Faker()

with app.app_context():
    print("Seeding database...")

    # Reset database
    db.drop_all()
    db.create_all()

    # Create dummy users
    user1 = User(username="testuser")
    user1.set_password("password123")

    user2 = User(username="patrick")
    user2.set_password("password12345")

    #add and save users to the db
    db.session.add_all([user1, user2])
    db.session.commit()

    #Create expenses for user1
    for _ in range(20):
        expense = Expense(
            title=fake.word(),
            amount=round(fake.random_number(digits=3), 2),
            category=fake.word(),
            description=fake.sentence(),
            user_id=user1.id
        )
        db.session.add(expense)

    # Create expenses for user2
    for _ in range(20):
        expense = Expense(
            title=fake.word(),
            amount=round(fake.random_number(digits=3), 2),
            category=fake.word(),
            description=fake.sentence(),
            user_id=user2.id
        )
        db.session.add(expense)
    #save to database
    db.session.commit()

    print("Seeding completed successfully!")