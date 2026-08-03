from flask import Blueprint, jsonify, request, session
from sqlalchemy.exc import IntegrityError

from auth import current_user, login_required
from extensions import db
from models import Note, User


api = Blueprint("api", __name__)


def payload():
    data = request.get_json(silent=True)
    return data if isinstance(data, dict) else {}


def errors(messages, status=400):
    return jsonify({"errors": messages}), status


def validate_note(data, partial=False):
    validation_errors = []
    allowed = {"title", "content"}
    unknown = set(data) - allowed
    if unknown:
        validation_errors.append("Only title and content may be supplied.")
    for field in allowed:
        value = data.get(field)
        if not partial and field not in data:
            validation_errors.append(f"{field.capitalize()} is required.")
        elif field in data and (not isinstance(value, str) or not value.strip()):
            validation_errors.append(f"{field.capitalize()} must be a non-empty string.")
    return validation_errors


@api.post("/signup")
def signup():
    data = payload()
    username = data.get("username", "").strip() if isinstance(data.get("username", ""), str) else ""
    password = data.get("password")
    confirmation = data.get("password_confirmation")
    validation_errors = []
    if not 3 <= len(username) <= 80:
        validation_errors.append("Username must be between 3 and 80 characters.")
    if not isinstance(password, str) or len(password) < 8:
        validation_errors.append("Password must be at least 8 characters.")
    if password != confirmation:
        validation_errors.append("Password confirmation must match password.")
    if validation_errors:
        return errors(validation_errors)

    user = User(username=username)
    user.password = password
    db.session.add(user)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return errors(["Username is already taken."], 409)
    session.clear()
    session["user_id"] = user.id
    return jsonify(user.to_dict()), 201


@api.post("/login")
def login():
    data = payload()
    username, password = data.get("username"), data.get("password")
    user = User.query.filter_by(username=username).first() if isinstance(username, str) else None
    if user is None or not isinstance(password, str) or not user.authenticate(password):
        return errors(["Invalid username or password."], 401)
    session.clear()
    session["user_id"] = user.id
    return jsonify(user.to_dict()), 200


@api.get("/check_session")
def check_session():
    user = current_user()
    return jsonify(user.to_dict() if user else {}), 200


@api.delete("/logout")
def logout():
    session.clear()
    return jsonify({}), 200


@api.route("/notes", methods=["GET", "POST"])
@login_required
def notes():
    user = current_user()
    if request.method == "POST":
        data = payload()
        validation_errors = validate_note(data)
        if validation_errors:
            return errors(validation_errors)
        note = Note(title=data["title"].strip(), content=data["content"].strip(), user_id=user.id)
        db.session.add(note)
        db.session.commit()
        return jsonify(note.to_dict()), 201

    try:
        page = max(int(request.args.get("page", 1)), 1)
        per_page = min(max(int(request.args.get("per_page", 10)), 1), 100)
    except ValueError:
        return errors(["page and per_page must be integers."])
    pagination = Note.query.filter_by(user_id=user.id).order_by(Note.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    return jsonify({
        "notes": [note.to_dict() for note in pagination.items],
        "page": pagination.page,
        "per_page": pagination.per_page,
        "total": pagination.total,
        "pages": pagination.pages,
    })


@api.route("/notes/<int:note_id>", methods=["GET", "PATCH", "DELETE"])
@login_required
def note_by_id(note_id):
    note = Note.query.filter_by(id=note_id, user_id=current_user().id).first()
    if note is None:
        return jsonify({"error": "Note not found."}), 404
    if request.method == "GET":
        return jsonify(note.to_dict())
    if request.method == "DELETE":
        db.session.delete(note)
        db.session.commit()
        return "", 204

    data = payload()
    validation_errors = validate_note(data, partial=True)
    if validation_errors or not data:
        return errors(validation_errors or ["Provide title and/or content."])
    if "title" in data:
        note.title = data["title"].strip()
    if "content" in data:
        note.content = data["content"].strip()
    db.session.commit()
    return jsonify(note.to_dict())
