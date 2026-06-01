from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import generate_password_hash, check_password_hash

db = SQLAlchemy()

#create User Model
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    # create relationship
    expenses = db.relationship("Expense", back_populates="user",cascade="all, delete-orphan")
    
    # Hash user password
    def set_password(self, password):
        self.password_hash = generate_password_hash(password).decode("utf-8")

    # Check password
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
#create Expense model
class Expense(db.Model):
    __tablename__ = "expenses"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(80), nullable=True)
    description = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    # relationship with foreign key
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # relationship back to User
    user = db.relationship("User", back_populates="expenses")

    def to_dict(self):
        return {
        "id": self.id,
        "title": self.title,
        "amount": self.amount,
        "category": self.category,
        "description": self.description,
        "created_at": self.created_at
    }
    