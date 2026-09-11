from server import db
from server.app import app
from server.models.task import Task
from server.models.user import User


def seed_data():
	with app.app_context():
		user = User.query.filter_by(username="demo").first()
		if not user:
			user = User(username="demo", email="demo@example.com")
			user.set_password("demo123")
			db.session.add(user)
			db.session.flush()

		if not Task.query.filter_by(user_id=user.id).first():
			db.session.add(Task(
				title="Try the task API",
				description="Create, update, and delete a task.",
				user_id=user.id,
			))
		db.session.commit()


if __name__ == "__main__":
	seed_data()
