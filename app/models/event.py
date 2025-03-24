from app.extensions import db
from datetime import datetime

class Event(db.Model):
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    title = db.Column(db.String(120), nullable=False)
    event_date = db.Column(db.DateTime, nullable=False)
    reminded = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, title, event_date, user_id):
        self.title = title
        self.event_date = event_date
        self.user_id = user_id
