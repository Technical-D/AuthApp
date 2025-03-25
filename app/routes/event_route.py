from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User 
from app.models.event import Event
from flask import request, jsonify
from app.extensions import db
from datetime import datetime
from app.extensions import logger

event_bp = Blueprint("event", __name__)

@event_bp.route("/", methods=["GET"])
@jwt_required()
def get_events():
    user_id = get_jwt_identity()
    now = datetime.now()
    events = db.session.query(Event).filter(
        Event.user_id == user_id,
        Event.event_date >=  now
    ).order_by(
        Event.event_date.asc()
    ).all()

    return jsonify([{"title": event.title, "event_date": event.event_date.strftime("%Y-%m-%d %H:%M:%S"), "reminded": "Yes" if event.reminded else "No"} for event in events])

@event_bp.route("/add", methods=["POST"])
@jwt_required()
def add_events():
    user_id = get_jwt_identity()

    data = request.get_json()

    title = data.get("title")
    event_date_str = data.get("event_date")

    if not title:
        return jsonify({"error": "Title is required"}), 400
    
    if not event_date_str:
        return jsonify({"error": "Event date is required"}), 400

    try:
        if len(event_date_str) == 16:
            event_date = datetime.strptime(event_date_str, "%Y-%m-%d %H:%M")
        elif len(event_date_str) == 13:
            event_date = datetime.strptime(event_date_str, "%Y-%m-%d %H")
        elif len(event_date_str) == 10:
            event_date = datetime.strptime(event_date_str, "%Y-%m-%d")
        else:
            event_date = datetime.strptime(event_date_str, "%Y-%m-%d %H:%M:%S")
    except ValueError as e:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD, YYYY-MM-DD HH, or YYYY-MM-DD HH:MM:SS"}), 400

    if event_date <= datetime.now():
        return jsonify({"error": "Event date must be in the future"}), 400

    new_event = Event(title=title, event_date=event_date, user_id=user_id)

    try:
        db.session.add(new_event)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print("Error occured", str(e))
        return jsonify({"error": "An error occurred while adding the event"}), 500

    return jsonify({"message": "Event added sucessfully."}), 201