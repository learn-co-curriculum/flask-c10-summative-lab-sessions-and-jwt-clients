from flask import request, session
from flask_restful import Resource

from config import db
from helpers import find_owned, login_required, paginate
from models import Activity, Mood
from schemas import ActivitySchema, MoodSchema

activity_schema = ActivitySchema()
activities_schema = ActivitySchema(many=True)
mood_schema = MoodSchema()


def name_taken(name, exclude_id=None):
    """Check whether the logged-in user already has an activity with this name."""
    query = Activity.query.filter_by(user_id=session["user_id"], name=(name or "").strip())
    if exclude_id is not None:
        query = query.filter(Activity.id != exclude_id)
    return query.first() is not None
    class Activities(Resource):
    method_decorators = [login_required]

    def get(self):
        query = Activity.query.filter_by(user_id=session["user_id"]).order_by(Activity.name)
        return paginate(query, activities_schema), 200

    def post(self):
        data = request.get_json() or {}
        if isinstance(data.get("name"), str) and name_taken(data["name"]):
            return {"errors": ["You already have an activity with that name."]}, 422
        try:
            activity = Activity(name=data.get("name"), user_id=session["user_id"])
            db.session.add(activity)
            db.session.commit()
        except ValueError as error:
            db.session.rollback()
            return {"errors": [str(error)]}, 422
        return activity_schema.dump(activity), 201


class ActivityById(Resource):
    method_decorators = [login_required]

    def get(self, id):
        activity = find_owned(Activity, id)
        if not activity:
            return {"errors": ["Activity not found."]}, 404
        return activity_schema.dump(activity), 200

    def patch(self, id):
        activity = find_owned(Activity, id)
        if not activity:
            return {"errors": ["Activity not found."]}, 404
               data = request.get_json() or {}
        if "name" in data:
            if isinstance(data["name"], str) and name_taken(data["name"], exclude_id=id):
                return {"errors": ["You already have an activity with that name."]}, 422
            try:
                activity.name = data["name"]
                db.session.commit()
            except ValueError as error:
                db.session.rollback()
                return {"errors": [str(error)]}, 422
        return activity_schema.dump(activity), 200

    def delete(self, id):
        activity = find_owned(Activity, id)
        if not activity:
            return {"errors": ["Activity not found."]}, 404
        db.session.delete(activity)
        db.session.commit()
        return {}, 204
        class MoodActivityLink(Resource):
    """Attach an activity to a mood (POST) or detach it (DELETE)."""
    method_decorators = [login_required]

    def _find_both(self, mood_id, activity_id):
        mood = find_owned(Mood, mood_id)
        activity = find_owned(Activity, activity_id)
        if not mood or not activity:
            return None, None, ({"errors": ["Mood or activity not found."]}, 404)
        return mood, activity, None

    def post(self, mood_id, activity_id):
        mood, activity, error = self._find_both(mood_id, activity_id)
        if error:
            return error
        if activity not in mood.activities:
            mood.activities.append(activity)
            db.session.commit()
        return mood_schema.dump(mood), 200

    def delete(self, mood_id, activity_id):
        mood, activity, error = self._find_both(mood_id, activity_id)
        if error:
            return error
        if activity in mood.activities:
            mood.activities.remove(activity)
            db.session.commit()
        return mood_schema.dump(mood), 200

