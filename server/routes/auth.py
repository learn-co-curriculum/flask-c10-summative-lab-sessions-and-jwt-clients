from flask import Blueprint, request, session
from models import db, User
from schemas import user_schema

auth_bp = Blueprint("auth", __name__)