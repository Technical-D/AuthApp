from flask import Flask, Blueprint
from app.routes.auth_routes import auth_bp
from app.routes.event_route import event_bp
from app.routes.profile_toute import profile_bp

def register_blueprints(app: Flask):
    """Register all blueprints."""
    app.register_blueprint(blueprint=auth_bp, url_prefix="/api/v1/auth/")
    app.register_blueprint(blueprint=profile_bp, url_prefix="/api/v1/user/")
    app.register_blueprint(blueprint=event_bp, url_prefix="/api/v1/events/")

    