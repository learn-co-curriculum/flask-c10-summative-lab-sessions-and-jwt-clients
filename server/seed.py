from server.app import app
from server.models import (
    User,
    Task,
    db,
)


with app.app_context():
    print(
        "Deleting existing data..."
    )

    Task.query.delete()
    User.query.delete()

    db.session.commit()

    print("Creating users...")

    christin = User(
        username="christin115"
    )
    christin.password = "password123"

    alex = User(
        username="alex_dev"
    )
    alex.password = "password123"

    jordan = User(
        username="jordan_codes"
    )
    jordan.password = "password123"

    db.session.add_all(
        [
            christin,
            alex,
            jordan,
        ]
    )

    db.session.commit()

    print("Creating tasks...")

    tasks = [
        Task(
            title=(
                "Complete authentication"
            ),
            description=(
                "Finish signup, login, "
                "logout, and check session."
            ),
            completed=True,
            user_id=christin.id,
        ),
        Task(
            title="Build task CRUD",
            description=(
                "Create protected task routes."
            ),
            completed=False,
            user_id=christin.id,
        ),
        Task(
            title="Add pagination",
            description=(
                "Paginate the task index."
            ),
            completed=False,
            user_id=christin.id,
        ),
        Task(
            title="Write README",
            description=(
                "Document the API."
            ),
            completed=False,
            user_id=christin.id,
        ),
        Task(
            title=(
                "Review Flask sessions"
            ),
            description=(
                "Practice session authentication."
            ),
            completed=True,
            user_id=alex.id,
        ),
        Task(
            title=(
                "Create Postman requests"
            ),
            description=(
                "Test all endpoints."
            ),
            completed=False,
            user_id=alex.id,
        ),
        Task(
            title="Plan weekly goals",
            description=(
                "Write goals for the week."
            ),
            completed=False,
            user_id=jordan.id,
        ),
    ]

    db.session.add_all(tasks)
    db.session.commit()

    print(
        "Database seeded successfully."
    )

    print(
        "Demo password: password123"
    )