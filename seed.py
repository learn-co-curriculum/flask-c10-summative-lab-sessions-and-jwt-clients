from app import app, db
from models import User, Note

with app.app_context():
    db.drop_all()
    db.create_all()
    user = User(username='testuser')
    user.set_password('password')
    db.session.add(user)
    db.session.commit()
    note1 = Note(title='First Note', content='This is your first note.', user_id=user.id)
    note2 = Note(title='Second Note', content='This is your second note.', user_id=user.id)
    db.session.add_all([note1, note2])
    db.session.commit()
    print('Seeded database!')