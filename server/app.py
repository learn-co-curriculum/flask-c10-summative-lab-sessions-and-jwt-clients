

"""
Notes app/Journal Entries
- Date/time last edited. If created: Date/Time created
- title
- body text
"""

from flask import Flask, make_response, jsonify, request, session
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import User, UserSchema, JournalEntry, JournalEntrySchema

app = Flask(__name__)

# using jwt