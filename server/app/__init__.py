"""
Application factory.

Using the factory pattern keeps the app object out of the global scope,
which makes testing and multiple-instance deployments straightforward.
"""
from flask import Flask
from app.config import Config
from app.extensions import db, migrate, bcrypt, cors


def create_app(config: Config = None) -> Flask:
    """Create and configure a Flask application instance.

    Args:
        config: A Config subclass (or instance).  When *None* the value of
                FLASK_ENV is used to pick the right class automatically.

    Returns:
        A fully-configured Flask application.
    """
    if config is None:
        from app.config import get_config
        config = get_config()

    app = Flask(__name__)
    app.config.from_object(config)

    # Initialise extensions
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    # Allow all origins in development; tighten in production via env vars
    cors.init_app(app, resources={r"/*": {"origins": "*"}})

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.notes import notes_bp
    from app.routes.tags import tags_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(notes_bp)
    app.register_blueprint(tags_bp)

    return app
