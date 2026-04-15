import os
from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_restful import Api, Resource
from marshmallow import ValidationError

from config import Config
from models import db, User, Note
from schemas import (
    UserSignupSchema,
    UserLoginSchema,
    NoteCreateSchema,
    NoteUpdateSchema,
)

bcrypt = Bcrypt()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    Migrate(app, db)
    JWTManager(app)
    api = Api(app)

    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        return jsonify({"errors": error.messages}), 400

    @app.errorhandler(404)
    def handle_not_found(error):
        return jsonify({"errors": ["Resource not found"]}), 404

    @app.route("/signup", methods=["POST"])
    def signup():
        payload = request.get_json() or {}
        schema = UserSignupSchema(context={"password": payload.get("password")})
        data = schema.load(payload)

        if User.query.filter_by(username=data["username"]).first():
            return jsonify({"errors": ["Username already exists"]}), 422

        password_digest = bcrypt.generate_password_hash(data["password"]).decode("utf-8")
        user = User(username=data["username"], password_digest=password_digest)
        db.session.add(user)
        db.session.commit()

        token = create_access_token(identity=str(user.id))
        return jsonify({"token": token, "user": user.to_dict()}), 201

    @app.route("/login", methods=["POST"])
    def login():
        payload = request.get_json() or {}
        data = UserLoginSchema().load(payload)
        user = User.query.filter_by(username=data["username"]).first()

        if not user or not bcrypt.check_password_hash(user.password_digest, data["password"]):
            return jsonify({"errors": ["Invalid username or password"]}), 401

        token = create_access_token(identity=str(user.id))
        return jsonify({"token": token, "user": user.to_dict()}), 200

    @app.route("/me", methods=["GET"])
    @jwt_required()
    def me():
        current_user_id = int(get_jwt_identity())
        user = User.query.get(current_user_id)
        if not user:
            return jsonify({"errors": ["User not found"]}), 404
        return jsonify(user.to_dict()), 200

    class NoteListResource(Resource):
        @jwt_required()
        def get(self):
            current_user_id = int(get_jwt_identity())
            page = int(request.args.get("page", 1))
            per_page = int(request.args.get("per_page", 10))

            notes_page = Note.query.filter_by(user_id=current_user_id).order_by(Note.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
            results = [note.to_dict() for note in notes_page.items]

            return {
                "notes": results,
                "meta": {
                    "page": notes_page.page,
                    "per_page": notes_page.per_page,
                    "total": notes_page.total,
                    "pages": notes_page.pages,
                },
            }, 200

        @jwt_required()
        def post(self):
            current_user_id = int(get_jwt_identity())
            payload = request.get_json() or {}
            data = NoteCreateSchema().load(payload)

            note = Note(user_id=current_user_id, **data)
            db.session.add(note)
            db.session.commit()
            return note.to_dict(), 201

    class NoteResource(Resource):
        @jwt_required()
        def patch(self, note_id):
            current_user_id = int(get_jwt_identity())
            note = Note.query.filter_by(id=note_id, user_id=current_user_id).first()
            if not note:
                return jsonify({"errors": ["Note not found"]}), 404

            payload = request.get_json() or {}
            data = NoteUpdateSchema().load(payload)
            for key, value in data.items():
                setattr(note, key, value)
            db.session.commit()
            return note.to_dict(), 200

        @jwt_required()
        def delete(self, note_id):
            current_user_id = int(get_jwt_identity())
            note = Note.query.filter_by(id=note_id, user_id=current_user_id).first()
            if not note:
                return jsonify({"errors": ["Note not found"]}), 404

            db.session.delete(note)
            db.session.commit()
            return {}, 204

    api.add_resource(NoteListResource, "/notes")
    api.add_resource(NoteResource, "/notes/<int:note_id>")

    return app


if __name__ == "__main__":
    application = create_app()
    application.run(host="0.0.0.0", port=int(os.environ.get("PORT", 3000)), debug=True)
