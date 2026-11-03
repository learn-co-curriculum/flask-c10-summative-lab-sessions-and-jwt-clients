from flask import request, session
from flask_restful import Resource

from config import db
from helpers import find_owned, login_required, paginate
from models import Journal
from schemas import JournalSchema

journal_schema = JournalSchema()
journals_schema = JournalSchema(many=True)

EDITABLE_FIELDS = ("title", "content")


class Journals(Resource):
    method_decorators = [login_required]

    def get(self):
        query = Journal.query.filter_by(user_id=session["user_id"]).order_by(
            Journal.created_at.desc(), Journal.id.desc()
        )
        return paginate(query, journals_schema), 200
        def post(self):
        data = request.get_json() or {}
        try:
            journal = Journal(
                title=data.get("title"),
                content=data.get("content"),
                user_id=session["user_id"],
            )
            db.session.add(journal)
            db.session.commit()
        except ValueError as error:
            db.session.rollback()
            return {"errors": [str(error)]}, 422
        return journal_schema.dump(journal), 201


class JournalById(Resource):
    method_decorators = [login_required]

    def get(self, id):
        journal = find_owned(Journal, id)
        if not journal:
            return {"errors": ["Journal entry not found."]}, 404
        return journal_schema.dump(journal), 200

    def patch(self, id):
        journal = find_owned(Journal, id)
        if not journal:
            return {"errors": ["Journal entry not found."]}, 404
 data = request.get_json() or {}
        try:
            for field in EDITABLE_FIELDS:
                if field in data:
                    setattr(journal, field, data[field])
            db.session.commit()
        except ValueError as error:
            db.session.rollback()
            return {"errors": [str(error)]}, 422
        return journal_schema.dump(journal), 200

    def delete(self, id):
        journal = find_owned(Journal, id)
        if not journal:
            return {"errors": ["Journal entry not found."]}, 404
        db.session.delete(journal)
        db.session.commit()
        return {}, 204