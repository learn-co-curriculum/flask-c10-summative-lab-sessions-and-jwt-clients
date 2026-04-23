"""

All routes are protected by JWT authentication.  Users can only manage their
own tags.

Endpoint summary
----------------
  GET    /tags          — list all tags for the current user
  POST   /tags          — create a new tag
  GET    /tags/<id>     — retrieve a single tag
  PATCH  /tags/<id>     — update a tag's name or colour
  DELETE /tags/<id>     — delete a tag (notes keep their tag_id as NULL)
"""
from flask import Blueprint, request

from app.extensions import db
from app.models.note import Tag
from app.utils.decorators import token_required
from app.utils.responses import ok, created, no_content, bad_request, not_found, server_error

tags_bp = Blueprint("tags", __name__, url_prefix="/tags")

# Allowed hex colour pattern (7-char, e.g. #3B82F6)
import re
_HEX_COLOR_RE = re.compile(r"^#[0-9A-Fa-f]{6}$")


# ------------------------------------------------------------------ #
# GET /tags                                                            #
# ------------------------------------------------------------------ #


@tags_bp.route("", methods=["GET"])
@token_required
def list_tags(current_user):
    """Return all tags belonging to the authenticated user."""
    tags = Tag.query.filter_by(user_id=current_user.id).order_by(Tag.name).all()
    return ok({"tags": [tag.to_dict() for tag in tags]})


# ------------------------------------------------------------------ #
# POST /tags                                                           #
# ------------------------------------------------------------------ #


@tags_bp.route("", methods=["POST"])
@token_required
def create_tag(current_user):
    """Create a new tag for the authenticated user."""
    data = request.get_json(silent=True) or {}

    name = (data.get("name") or "").strip()
    color = (data.get("color") or "#3B82F6").strip()

    errors = []
    if not name:
        errors.append("Tag name is required.")
    if len(name) > 80:
        errors.append("Tag name must not exceed 80 characters.")
    if not _HEX_COLOR_RE.match(color):
        errors.append("Color must be a valid 6-digit hex value (e.g. #3B82F6).")
    if errors:
        return bad_request("Validation failed.", errors)

    # Uniqueness per user
    if Tag.query.filter_by(user_id=current_user.id, name=name).first():
        return bad_request("Validation failed.", ["You already have a tag with that name."])

    try:
        tag = Tag(user_id=current_user.id, name=name, color=color)
        db.session.add(tag)
        db.session.commit()
    except Exception:
        db.session.rollback()
        return server_error("Could not create tag. Please try again.")

    return created(tag.to_dict())


# ------------------------------------------------------------------ #
# GET /tags/<id>                                                       #
# ------------------------------------------------------------------ #


@tags_bp.route("/<int:tag_id>", methods=["GET"])
@token_required
def get_tag(current_user, tag_id):
    """Return a single tag owned by the authenticated user."""
    tag = Tag.query.filter_by(id=tag_id, user_id=current_user.id).first()
    if tag is None:
        return not_found("Tag not found.")
    return ok(tag.to_dict())


# ------------------------------------------------------------------ #
# PATCH /tags/<id>                                                     #
# ------------------------------------------------------------------ #


@tags_bp.route("/<int:tag_id>", methods=["PATCH"])
@token_required
def update_tag(current_user, tag_id):
    """Partially update a tag's name or colour."""
    tag = Tag.query.filter_by(id=tag_id, user_id=current_user.id).first()
    if tag is None:
        return not_found("Tag not found.")

    data = request.get_json(silent=True) or {}
    errors = []

    if "name" in data:
        name = (data["name"] or "").strip()
        if not name:
            errors.append("Tag name must not be blank.")
        elif len(name) > 80:
            errors.append("Tag name must not exceed 80 characters.")
        else:
            # Check uniqueness (excluding the current tag)
            duplicate = Tag.query.filter(
                Tag.user_id == current_user.id,
                Tag.name == name,
                Tag.id != tag_id,
            ).first()
            if duplicate:
                errors.append("You already have a tag with that name.")
            else:
                tag.name = name

    if "color" in data:
        color = (data["color"] or "").strip()
        if not _HEX_COLOR_RE.match(color):
            errors.append("Color must be a valid 6-digit hex value (e.g. #3B82F6).")
        else:
            tag.color = color

    if errors:
        return bad_request("Validation failed.", errors)

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        return server_error("Could not update tag. Please try again.")

    return ok(tag.to_dict())


# ------------------------------------------------------------------ #
# DELETE /tags/<id>                                                    #
# ------------------------------------------------------------------ #


@tags_bp.route("/<int:tag_id>", methods=["DELETE"])
@token_required
def delete_tag(current_user, tag_id):
    """Delete a tag.  Associated notes retain their tag_id as NULL."""
    tag = Tag.query.filter_by(id=tag_id, user_id=current_user.id).first()
    if tag is None:
        return not_found("Tag not found.")

    try:
        db.session.delete(tag)
        db.session.commit()
    except Exception:
        db.session.rollback()
        return server_error("Could not delete tag. Please try again.")

    return no_content()
