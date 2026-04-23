"""
Notes CRUD routes.

All routes require a valid JWT (enforced by ``@token_required``).  Users can
only read and modify their own notes; attempts to access another user's note
return 404 rather than 403 to avoid leaking resource existence.

"""
from flask import Blueprint, request, current_app

from app.extensions import db
from app.models.note import Note
from app.utils.decorators import token_required
from app.utils.responses import ok, created, no_content, bad_request, not_found, server_error

notes_bp = Blueprint("notes", __name__, url_prefix="/notes")


# ------------------------------------------------------------------ #
# GET /notes                                                           #
# ------------------------------------------------------------------ #


@notes_bp.route("", methods=["GET"])
@token_required
def list_notes(current_user):
    """Return a paginated list of the authenticated user's notes.

    Query parameters
    ----------------
    page     : int  — 1-based page number (default 1)
    per_page : int  — items per page (default from config, max 100)
    pinned   : bool — if "true", return only pinned notes
    """
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get(
        "per_page", current_app.config["ITEMS_PER_PAGE"], type=int
    )
    pinned_filter = request.args.get("pinned", None)

    # Guard against out-of-range values
    page = max(1, page)
    per_page = min(max(1, per_page), current_app.config["MAX_ITEMS_PER_PAGE"])

    query = Note.query.filter_by(user_id=current_user.id)

    if pinned_filter is not None:
        query = query.filter_by(pinned=(pinned_filter.lower() == "true"))

    # Pinned notes float to the top; within each group sort by newest first
    query = query.order_by(Note.pinned.desc(), Note.created_at.desc())

    paginated = query.paginate(page=page, per_page=per_page, error_out=False)

    return ok(
        {
            "notes": [note.to_dict() for note in paginated.items],
            "total": paginated.total,
            "pages": paginated.pages,
            "current_page": page,
            "per_page": per_page,
        }
    )


# ------------------------------------------------------------------ #
# POST /notes                                                          #
# ------------------------------------------------------------------ #


@notes_bp.route("", methods=["POST"])
@token_required
def create_note(current_user):
    """Create a new note owned by the authenticated user."""
    data = request.get_json(silent=True) or {}

    title = (data.get("title") or "").strip()
    content = (data.get("content") or "").strip()
    pinned = bool(data.get("pinned", False))
    tag_id = data.get("tag_id")

    errors = []
    if not title:
        errors.append("Title is required.")
    if len(title) > 255:
        errors.append("Title must not exceed 255 characters.")
    if not content:
        errors.append("Content is required.")
    if errors:
        return bad_request("Validation failed.", errors)

    try:
        note = Note(
            user_id=current_user.id,
            title=title,
            content=content,
            pinned=pinned,
            tag_id=tag_id,
        )
        db.session.add(note)
        db.session.commit()
    except Exception:
        db.session.rollback()
        return server_error("Could not create note. Please try again.")

    return created(note.to_dict())


# ------------------------------------------------------------------ #
# GET /notes/<id>                                                      #
# ------------------------------------------------------------------ #


@notes_bp.route("/<int:note_id>", methods=["GET"])
@token_required
def get_note(current_user, note_id):
    """Return a single note.  Returns 404 if not found or not owned."""
    note = Note.owned_by(note_id, current_user.id)
    if note is None:
        return not_found("Note not found.")
    return ok(note.to_dict())


# ------------------------------------------------------------------ #
# PATCH /notes/<id>                                                    #
# ------------------------------------------------------------------ #


@notes_bp.route("/<int:note_id>", methods=["PATCH"])
@token_required
def update_note(current_user, note_id):
    """Partially update a note.  Only supplied fields are changed."""
    note = Note.owned_by(note_id, current_user.id)
    if note is None:
        return not_found("Note not found.")

    data = request.get_json(silent=True) or {}
    errors = []

    if "title" in data:
        title = (data["title"] or "").strip()
        if not title:
            errors.append("Title must not be blank.")
        elif len(title) > 255:
            errors.append("Title must not exceed 255 characters.")
        else:
            note.title = title

    if "content" in data:
        content = (data["content"] or "").strip()
        if not content:
            errors.append("Content must not be blank.")
        else:
            note.content = content

    if "pinned" in data:
        note.pinned = bool(data["pinned"])

    if "tag_id" in data:
        note.tag_id = data["tag_id"]

    if errors:
        return bad_request("Validation failed.", errors)

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        return server_error("Could not update note. Please try again.")

    return ok(note.to_dict())


# ------------------------------------------------------------------ #
# DELETE /notes/<id>                                                   #
# ------------------------------------------------------------------ #


@notes_bp.route("/<int:note_id>", methods=["DELETE"])
@token_required
def delete_note(current_user, note_id):
    """Delete a note.  Returns 204 No Content on success."""
    note = Note.owned_by(note_id, current_user.id)
    if note is None:
        return not_found("Note not found.")

    try:
        db.session.delete(note)
        db.session.commit()
    except Exception:
        db.session.rollback()
        return server_error("Could not delete note. Please try again.")

    return no_content()
