from datetime import datetime, timedelta, timezone
from app.extensions import db

def utc_now():
    """Returns the current UTC time with timezone info."""
    return datetime.now(timezone.utc)

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    otp = db.Column(db.String(6), nullable=True)
    otp_expiry = db.Column(db.DateTime, nullable=True)
    is_verified = db.Column(db.Boolean, default=False)  
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def set_otp(self, otp):
        self.otp = otp
        # Assuming you want to store the time in UTC
        self.otp_expiry = datetime.now(timezone.utc) + timedelta(minutes=5)

    def is_otp_valid(self, otp):
        if self.otp_expiry and self.otp_expiry.tzinfo is None:
            self.otp_expiry = self.otp_expiry.replace(tzinfo=timezone.utc)  # Convert to UTC-aware datetime
        
        current_time = datetime.now(timezone.utc)
        return self.otp == str(otp) and current_time < self.otp_expiry
