from server.extensions import db, bcrypt
from server.models.base_model import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    tasks = db.relationship("Task", back_populates="user",cascade="all, delete-orphan",lazy=True)

    @property
    def password(self):
        raise AttributeError("Password is write-only.")

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash,password)

    def to_dict(self):
        user_dict = super().to_dict()
        user_dict.update({
            'id': self.id,
            'username': self.username,
        })
        return user_dict

    def __repr__(self):
        return f"<User {self.username}>"
