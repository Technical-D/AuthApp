from flask import Blueprint, request, jsonify
from app.extensions import db, limiter
from app.models.user import User
import random
from flask_jwt_extended import create_access_token
from app.services.mail_service import send_otp_email
import re

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    email = data.get("email")
    name = data.get("name")

    if not email:
        return jsonify({"error": "Email is required"})
    
    if not name:
        return jsonify({"error": "Name is required"})

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "User already exists"}), 400

    new_user = User(email=email, name=name)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully!"}), 201

@auth_bp.route("/send-otp", methods=["POST"])
@limiter.limit("25 per hour")
def send_otp():
    data = request.get_json()
    email = data.get("email")
    if not email:
        return jsonify({"error": "Email is required"})
    
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return jsonify({"error": "Invalid email"}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    otp = str(random.randint(100000, 999999))  # Generates 6-digit OTP
    print(otp)
    user.set_otp(otp)

    if not send_otp_email(email, otp):
        db.session.rollback()
        return {"error": "Failed to send OTP"}, 500

    # Commiting chnages to db
    db.session.commit()

    return jsonify({"message": "OTP sent to your email. Use that to verify yourself.", "otp":otp}), 200

@auth_bp.route("/verify-otp", methods=["POST"])
def verify_otp():
    data = request.get_json()
    email = data.get("email")
    otp = data.get("otp")

    if not email:
        return jsonify({"error": "Email is required"}), 400
    
    if not otp:
        return jsonify({"error": "OTP is required"}), 400

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    if user.is_otp_valid(otp):
        user.is_verified = True
        user.otp = None 
        user.otp_expiry = None
        db.session.commit()
        
        access_token = create_access_token(identity=str(user.id))

        return jsonify({
            "message": "OTP verified successfully!",
            "token": access_token  
        })
    
    return jsonify({"error": "Invalid or expired OTP"}), 400
