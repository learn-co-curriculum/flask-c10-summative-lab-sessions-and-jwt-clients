from faker import Faker
from config import create_app, db
from models import User, Note

fake = Faker()

def seed_database():
    print("Seeding database...")

    # Clear existing data
    print("Clearing existing data...")
    Note.query.delete()
    User.query.delete()
    db.session.commit()

    # Create users
    print("Creating users...")
    users = []

    # Create a known test user for easy login
    test_user = User(
        username='testuser',
        email='testuser@example.com'
    )
    test_user.password_hash = 'password123'
    db.session.add(test_user)
    users.append(test_user)

    # Create additional fake users
    for _ in range(4):
        user = User(
            username=fake.unique.user_name(),
            email=fake.unique.email()
        )
        user.password_hash = 'password123'
        db.session.add(user)
        users.append(user)

    db.session.commit()
    print(f"Created {len(users)} users.")

    # Create notes for each user
    print("Creating notes...")
    note_count = 0

    for user in users:
        # Create between 5 and 10 notes per user
        for _ in range(fake.random_int(min=5, max=10)):
            note = Note(
                title=fake.sentence(nb_words=5),
                content=fake.paragraph(nb_sentences=3),
                user_id=user.id
            )
            db.session.add(note)
            note_count += 1

    db.session.commit()
    print(f"Created {note_count} notes.")
    print("Done seeding!")


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        seed_database()