"""
config.py
---------
Central configuration module for the Flask Notes API.

Initialises and exposes:
    - app       : Flask application instance
    - db        : SQLAlchemy database instance
    - bcrypt    : Flask-Bcrypt instance for password hashing
    - migrate   : Flask-Migrate instance for database migrations
    - api       : Flask-RESTful API instance

All other modules import from here to prevent circular imports.
"""

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

# ── Flask application ─────────────────────────────────────────────────────────
app = Flask(__name__)

# Secret key used to cryptographically sign session cookies.
# In production this should be loaded from an environment variable.
app.secret_key = b'\x92\x14\xa3\xf7\x88\x01\xbc\xd4eQ\x80t \xca\x1a\x10K'

# ── Database configuration ────────────────────────────────────────────────────
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Return JSON responses with readable indentation
app.json.compact = False

# ── Extension instances ───────────────────────────────────────────────────────
db      = SQLAlchemy()
bcrypt  = Bcrypt(app)
migrate = Migrate(app, db)
api     = Api(app)

# Bind SQLAlchemy to the Flask app
db.init_app(app)