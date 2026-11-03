from flask import request, session
from flask_restful import Resource

from config import db
from helpers import find_owned, login_required, paginate
from models import Mood
from schemas import MoodSchema

mood_schema = MoodSchema()
moods_schema = MoodSchema(many=True)

EDITABLE_FIELDS = ("mood", "intensity", "note")


class Moods(Resource):
    method_decorators = [login_required]

    def get(self):
        query = Mood.query.filter_by(user_id=session["user_id"]).order_by(
            Mood.created_at.desc(), Mood.id.desc()
        )
        return paginate(query, moods_schema), 200

    def post(self):
        data = request.get_json() or {}
        try:
            mood = Mood(
                mood=data.get("mood"),
                intensity=data.get("intensity"),
                note=data.get("note"),
                user_id=session["user_id"],
            )
            db.session.add(mood)
            db.session.commit()
        except ValueError as error:
            db.session.rollback()
            return {"errors": [str(error)]}, 422
        return mood_schema.dump(mood), 201


class MoodById(Resource):
    method_decorators = [login_required]

    def get(self, id):
        mood = find_owned(Mood, id)
        if not mood:
            return {"errors": ["Mood not found."]}, 404
        return mood_schema.dump(mood), 200

    def patch(self, id):
        mood = find_owned(Mood, id)
        if not mood:
            return {"errors": ["Mood not found."]}, 404

        data = request.get_json() or {}
        try:
            for field in EDITABLE_FIELDS:
                if field in data:
                    setattr(mood, field, data[field])
            db.session.commit()
        except ValueError as error:
            db.session.rollback()
            return {"errors": [str(error)]}, 422
        return mood_schema.dump(mood), 200

    def delete(self, id):
        mood = find_owned(Mood, id)
        if not mood:
            return {"errors": ["Mood not found."]}, 404
        db.session.delete(mood)
        db.session.commit()
        return {}, 204