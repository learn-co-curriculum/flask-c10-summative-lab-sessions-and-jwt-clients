"""Routes package — exports all blueprints."""
from app.routes.auth import auth_bp
from app.routes.notes import notes_bp
from app.routes.tags import tags_bp

__all__ = ["auth_bp", "notes_bp", "tags_bp"]
