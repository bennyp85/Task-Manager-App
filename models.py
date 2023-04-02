from datetime import datetime
from init import db

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    due_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    priority_level = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'<Task {self.name}>'
