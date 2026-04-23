from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=True, unique=True)
    password_hash = db.Column(db.String, nullable=False)
    
    expenses = db.relationship('Expense', back_populates = 'user', cascade = 'all, delete-orphan')
    
    @validates('username')
    def validate_username(self, key, value):
        if not value or len(value.strip()) == 0:
            raise ValueError("Username cannot be empty.")
        return value
    
    @validates('email')
    def validate_email(self, key, value):
        if '@' not in value:
            raise ValueError("Invalid Email address, please enter an ACTUAL email address")
        return value
        
    def __repr__ (self):
        return f'<User {self.username}>'
        

class Expense(db.Model):
    __tablename__ = 'expenses'
    
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    title = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    user = db.relationship('User', back_populates='expenses')
    
    @validates('amount')
    def validate_amount(self, key, value):
        if value is None or value <= 0:
            raise ValueError("Amount must be greater than zero.")
        return value
    
    @validates('title')
    def validate_title(self, key, value):
        if not value or len(value.strip()) == 0:
            raise ValueError("Title can't be empty.")
        return value
    
    @validates('category')
    def validate_category(self, key, value):
        allowed = ['food', 'transport', 'entertainment', 'utilities', 'health', 'other']
        if value.lower() not in allowed:
            raise ValueError(f"Category must be one of the following: {', '.join(allowed)}")
        return value.lower()
    
    def __repr__(self):
        return f'<Expense {self.title} - Ksh{self.amount}>'