from faker import Faker

from server.app import app
from server.models import db, User, Note

fake = Faker()


def seed_data():
    with app.app_context():
        print("Deleting old data...")

        db.session.query(Note).delete()
        db.session.query(User).delete()
        db.session.commit()

        print("Creating users...")

        users = []

        for _ in range(3):
            user = User(username=fake.user_name())
            user.password_hash = "password123"

            db.session.add(user)
            users.append(user)

        db.session.commit()

        print("Creating notes...")

        categories = [
            "Personal",
            "Work",
            "Ideas",
            "Tasks",
            "Journal"
        ]

        for user in users:
            for _ in range(5):
                note = Note(
                    title=fake.sentence(nb_words=5),
                    content=fake.paragraph(nb_sentences=3),
                    category=fake.random_element(categories),
                    user_id=user.id
                )
                db.session.add(note)

        db.session.commit()

        print("Database seeded successfully!")


if __name__ == "__main__":
    seed_data()