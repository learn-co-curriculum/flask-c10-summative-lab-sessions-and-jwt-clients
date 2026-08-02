from server.extensions import db
from server.models.base_model import BaseModel

class Task(BaseModel):
    __tablename__ = 'tasks'
    
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    due_date = db.Column(db.Date, nullable=True)
    completed = db.Column(db.Boolean, default=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    user = db.relationship('User', back_populates='tasks', foreign_keys=[user_id])

    def to_dict(self):
        task_dict = super().to_dict()
        task_dict.update({
            'title': self.title,
            'description': self.description,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'completed': self.completed,
            'user_id': self.user_id,
        })
        return task_dict