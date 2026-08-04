import random
from faker import Faker
from app import create_app, db
from app.models import User, Note

faker = Faker()

app = create_app("development")