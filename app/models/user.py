from datetime import datetime, timedelta, timezone
from app.extensions import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    otp = db.Column(db.String(6), nullable=True)
    otp_expiry = db.Column(db.DateTime, nullable=True)
    is_verified = db.Column(db.Boolean, default=False)  
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    events = db.relationship("Event", backref="user", lazy=True)

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def set_otp(self, otp):
        self.otp = otp
        self.otp_expiry = datetime.now() + timedelta(minutes=5)

    def is_otp_valid(self, otp):  
        current_time = datetime.now()
        return self.otp == str(otp) and current_time < self.otp_expiry
