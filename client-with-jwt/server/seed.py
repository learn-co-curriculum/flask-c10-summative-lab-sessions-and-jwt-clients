from faker import Faker
from server import create_app, db
from server.models import User, Recipe

app = create_app()
fake = Faker()