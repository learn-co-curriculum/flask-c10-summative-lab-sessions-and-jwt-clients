from flask import request, session
from flask_restful import Resource
from datetime import datetime

from config import app, api, db
from models import (
    User,
    Workout, 
    user_schema,
    workout_schema, 
    workouts_schema,
)


@app.before_request
def check_if_logged_in():
    open_access_list = [
        "signup",
        "login",
        "checksession"
    ]

    if request.endpoint not in open_access_list and "user_id" not in session:
        return {"error": "Unauthorized"}, 401

#Sign up route
class Signup(Resource):
    def post(self):
        data = request.get_json()

        username = data.get("username")
        password = data.get("password")
        password_confirmation = data.get("password_confirmation")

        #Password must match password_confirmation
        if password != password_confirmation:
            return{
                "errors": ["Passwords do not match."]
            }, 422

        # Making sure the username does not belong to another user
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return {
                "errors": ["Username already exists."]
            }, 422
        user = User(
                username=username
            )
        user.password_hash = password

        db.session.add(user)
        db.session.commit()

        session["user_id"] = user.id
        return user_schema.dump(user), 201
#Checking session
class CheckSession(Resource):
    def get(self):
        user = User.query.filter_by(
            id=session["user_id"]
        ).first()
        if not user:
            return{'error': 'unauthorized'}, 401
        return user_schema.dump(user), 200

class Login(Resource):
    def post(self):
        data = request.get_json()

        username = data.get("username")
        password = data.get("password")
        user = User.query.filter_by(
            username=username
        ).first()
        if not user or not user.authenticate(password):
            return {
                "errors": ["Invalid username or password."]
            }, 401

        session["user_id"] = user.id

        return user_schema.dump(user), 200
#Logging the user out
class Logout(Resource):
    def delete(self):
            session.clear()
            return {}, 204

#Accessing workouts and pagination
class WorkoutList(Resource):
    def get(self):
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 5, type=int)

        workouts = Workout.query.filter_by(
            user_id=session["user_id"]
        ).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )

        return workouts_schema.dump(workouts.items), 200   
    def post(self):
        data = request.get_json()
        workout = Workout(
        title=data["title"],
        duration=data["duration"],
        date=datetime.strptime(data["date"], "%Y-%m-%d").date(),
        user_id=session["user_id"]
        )

        db.session.add(workout)
        db.session.commit()
        return workout_schema.dump(workout), 201

class WorkoutByID(Resource):

    #Getting Workout by Id and confirming it belongs to user
    def get(self, id):
        workout = Workout.query.filter_by(
            id=id,
            user_id=session["user_id"]
        ).first()
        if not workout:
            return {"error": "Workout not found."}, 404
        return workout_schema.dump(workout), 200

    #Editing workout details
    def patch(self, id):
        workout = Workout.query.filter_by(
            id=id,
            user_id=session["user_id"]
        ).first()
        if not workout:
            return {"error": "Workout not found."}, 404
        data = request.get_json()
        if "title" in data:
            workout.title = data["title"]
        if "duration" in data:
            workout.duration = data["duration"]
        if "date" in data:
            workout.date = datetime.strptime(
                data["date"],
                "%Y-%m-%d"
            ).date()
        db.session.commit()
        return workout_schema.dump(workout), 200

    #Deleting Workout
    def delete(self, id):
        workout = Workout.query.filter_by(
            id=id,
            user_id=session["user_id"]
        ).first()
        if not workout:
            return {"error": "Workout not found."}, 404
        db.session.delete(workout)
        db.session.commit()
        return {}, 204




api.add_resource(Signup, '/signup')
api.add_resource(CheckSession, "/check_session")
api.add_resource(Login, "/login")
api.add_resource(Logout, "/logout")
api.add_resource(WorkoutList, "/workouts")
api.add_resource(WorkoutByID, "/workouts/<int:id>")
if __name__ == '__main__':
    app.run(port=5555, debug=True)
        




