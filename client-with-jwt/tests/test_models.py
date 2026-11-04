
import pytest
from sqlalchemy.exc import IntegrityError

from server.models import db, User, Recipe


def test_password_is_hashed(app):
    with app.app_context():
        user = User(username="chef_model")
        user.password = "password123"
        assert user._password_hash != "password123"


def test_username_must_be_unique(app):
    with app.app_context():
        first = User(username="dupe_chef")
        first.password = "password123"
        db.session.add(first)
        db.session.commit()

        second = User(username="dupe_chef")
        second.password = "password123"
        db.session.add(second)
        with pytest.raises(IntegrityError):
            db.session.commit()
        db.session.rollback()


def test_recipe_belongs_to_user(app):
    with app.app_context():
        user = User(username="owner_chef")
        user.password = "password123"
        db.session.add(user)
        db.session.commit()

        recipe = Recipe(
            title="Toast",
            instructions="Toast the bread.",
            prep_time_minutes=5,
            ingredients="Bread",
            user_id=user.id,
        )
        db.session.add(recipe)
        db.session.commit()

        assert recipe.user_id == user.id
