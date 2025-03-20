import jwt
from datetime import datetime, timezone, timedelta
from flask import current_app

def generate_jwt(user):
    """
    Generate a JWT token for the given user.
    """
    expiration_time = datetime.now(timezone.utc) + timedelta(hours=1)  # 1 hour expiration
    payload = {
        "sub": str(user.id),
        "email": user.email,
        "exp": expiration_time
    }
    
    # You should have a secret key in your app's config
    token = jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')
    return token

def decode_jwt(token):
    """
    Decode a JWT token and return the user ID and email.
    """
    try:
        payload = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None  # Token expired
    except jwt.InvalidTokenError:
        return None  # Invalid token
