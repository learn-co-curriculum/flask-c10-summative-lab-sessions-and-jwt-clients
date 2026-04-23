"""
Database seed script.

Run with:
    python seed.py

Drops all tables, recreates them, and inserts sample data.
"""

from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.note import Note, Tag

app = create_app()

with app.app_context():
    print("Dropping all tables...")
    db.drop_all()

    print("Creating all tables...")
    db.create_all()

    # ------------------------------------------------------------------ #
    # Users                                                                #
    # ------------------------------------------------------------------ #

    user1 = User(username="alice@example.com")
    user1.set_password("password123")

    user2 = User(username="bob@example.com")
    user2.set_password("password123")

    db.session.add_all([user1, user2])
    db.session.commit()
    print(f"Created users: {user1.username}, {user2.username}")

    # ------------------------------------------------------------------ #
    # Tags                                                                 #
    # ------------------------------------------------------------------ #

    tag_work = Tag(name="Work", user_id=user1.id)
    tag_personal = Tag(name="Personal", user_id=user1.id)
    tag_ideas = Tag(name="Ideas", user_id=user2.id)

    db.session.add_all([tag_work, tag_personal, tag_ideas])
    db.session.commit()
    print("Created tags.")

    # ------------------------------------------------------------------ #
    # Notes                                                                #
    # ------------------------------------------------------------------ #

    notes = [
        Note(
            title="Project kickoff",
            content="Set up repo, install dependencies, configure linting.",
            pinned=True,
            user_id=user1.id,
            tag_id=tag_work.id,
        ),
        Note(
            title="Meeting notes",
            content="Discussed sprint goals. Action items assigned to team.",
            pinned=False,
            user_id=user1.id,
            tag_id=tag_work.id,
        ),
        Note(
            title="Grocery list",
            content="Eggs, milk, bread, avocados, coffee.",
            pinned=False,
            user_id=user1.id,
            tag_id=tag_personal.id,
        ),
        Note(
            title="App idea",
            content="A habit tracker that integrates with Spotify mood data.",
            pinned=True,
            user_id=user2.id,
            tag_id=tag_ideas.id,
        ),
        Note(
            title="Reading list",
            content="Clean Code, The Pragmatic Programmer, Designing Data-Intensive Applications.",
            pinned=False,
            user_id=user2.id,
            tag_id=tag_ideas.id,
        ),
    ]

    db.session.add_all(notes)
    db.session.commit()
    print(f"Created {len(notes)} notes.")

    print("\nSeed complete!")
    print("  alice@example.com / password123")
    print("  bob@example.com   / password123")
