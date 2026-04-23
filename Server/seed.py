from app import app, bcrypt
from models import db, User, Expense

with app.app_context():
    Expense.query.delete()
    User.query.delete()
    db.session.commit()
    
    u1 = User(
        username = 'Gene',
        email = 'Gene.test@fakemail.com',
        password_hash = bcrypt.generate_password_hash('password678').decode('utf-8')
    )
    u2 = User(
        username = 'Grace',
        email = 'Grace.test@fakemail.com',
        password_hash = bcrypt.generate_password_hash('password456').decode('utf-8')
    )
    
    db.session.add_all([u1, u2])
    db.session.commit()
    
    expenses = [
        Expense(title='Groceries', amount=45.50, category='food', user_id=u1.id),
        Expense(title='Bus fare', amount=2.50, category='transport', user_id=u1.id),
        Expense(title='Netflix', amount=15.00, category='entertainment', user_id=u1.id),
        Expense(title='Gym', amount=30.00, category='health', user_id=u1.id),
        Expense(title='Electricity', amount=60.00, category='utilities', user_id=u1.id),
        Expense(title='Lunch', amount=12.00, category='food', user_id=u2.id),
        Expense(title='Uber', amount=8.00, category='transport', user_id=u2.id),
    ]
    
    db.session.add_all(expenses)
    db.session.commit()
    
    print("Seeding complete!!")
