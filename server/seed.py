from app import app
from config import db
from models import User, Task

with app.app_context():


    Task.query.delete()
    User.query.delete()

    user1 = User(username="wanjohi")
    user1.password = "password123"

    user2 =User(username="kamotho")
    user2.password = "password123"

    db.session.add_all([user1, user2])
    db.session.commit()


    task1 = Task(
        title = "Buy groceries",
        description = "Buy milk, bread, eggs, fruits and vegetables",
        completed = False,
        user_id = user1.id
    )

    task2 = Task(
        title = "Pay electricity bill",
        description = "Pay due bill before end of the week",
        completed = False,
        user_id = user1.id
    )

    task3 = Task(
        title = "Call the dentist",
        description = "Schedule my routine dental checkup",
        completed = True,
        user_id = user1.id
    )

    task4 = Task(
        title = "Clean the house",
        description = "Mop the floo and organise my living room",
        completed  = False,
        user_id = user2.id
    )

    task5 = Task(
        title = "Read a book",
        description = "Read two chapters of Things fall apart by Chinua Achebe",
        completed = False,
        user_id = user2.id
    )

    task6 = Task(
        title = "Morning run",
        description = "Run 5km in the hood",
        completed = True,
        user_id = user2.id
    )

    db.session.add_all([task1, task2, task3, task4, task5, task6])
    db.session.commit()

    print("Database seeded successfully!")