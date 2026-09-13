from flask import Blueprint, jsonify, request, g
from marshmallow import ValidationError

from models import db, ReadingEntry
from schemas import ReadingEntrySchema
from auth import login_required


resource = Blueprint("resource", __name__, url_prefix="/readings")

reading_schema = ReadingEntrySchema()
readings_schema = ReadingEntrySchema(many=True)


# GET /readings
@resource.get("")
@login_required
def get_readings():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    if page < 1 or per_page < 1 or per_page > 100:
        return jsonify(
            errors=["page must be >= 1 and per_page must be between 1 and 100."]
        ), 400

    pagination = db.paginate(
        ReadingEntry.query
        .filter(ReadingEntry.user_id == g.current_user.id)
        .order_by(ReadingEntry.id),
        page=page,
        per_page=per_page,
        error_out=False
    )

    return jsonify({
        "readings": readings_schema.dump(pagination.items),
        "page": pagination.page,
        "per_page": pagination.per_page,
        "pages": pagination.pages,
        "total": pagination.total
    }), 200


# POST /readings
@resource.post("")
@login_required
def create_reading():
    try:
        data = reading_schema.load(
            request.get_json(silent=True)
        )
    except ValidationError as exc:
        return jsonify(errors=exc.messages), 400

    reading = ReadingEntry(
        title=data["title"],
        author=data["author"],
        status=data["status"],
        rating=data.get("rating"),
        start_date=data.get("start_date"),
        completion_date=data.get("completion_date"),
        user_id=g.current_user.id
    )

    db.session.add(reading)
    db.session.commit()

    return jsonify(reading_schema.dump(reading)), 201


# PATCH /readings/<id>
@resource.patch("/<int:reading_id>")
@login_required
def update_reading(reading_id):
    reading = ReadingEntry.query.filter_by(
        id=reading_id,
        user_id=g.current_user.id
    ).first()

    if reading is None:
        return jsonify(errors=["Reading entry not found."]), 404

    try:
        data = reading_schema.load(
            request.get_json(silent=True),
            partial=True
        )
    except ValidationError as exc:
        return jsonify(errors=exc.messages), 400

    for field, value in data.items():
        setattr(reading, field, value)

    db.session.commit()

    return jsonify(reading_schema.dump(reading)), 200


# DELETE /readings/<id>
@resource.delete("/<int:reading_id>")
@login_required
def delete_reading(reading_id):
    reading = ReadingEntry.query.filter_by(
        id=reading_id,
        user_id=g.current_user.id
    ).first()

    if reading is None:
        return jsonify(errors=["Reading entry not found."]), 404

    db.session.delete(reading)
    db.session.commit()

    return "", 204