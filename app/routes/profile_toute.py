from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User
from flask import jsonify

profile_bp = Blueprint("profile", __name__)

@profile_bp.route("/profile", methods=["GET"])
@jwt_required() 
def profile():
    current_user_id = get_jwt_identity()  

    user = User.query.get(current_user_id)
    if user:
        return jsonify({
            "message": "Welcome to your profile!",
            "email": user.email,
            "name": user.name
        })
    else:
        return jsonify({"error": "User not found"}), 404