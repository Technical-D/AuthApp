from flask import Flask, Blueprint
from app.routes.auth_routes import auth_bp

def register_blueprints(app: Flask):
    """Register all blueprints."""
    app.register_blueprint(blueprint=auth_bp, url_prefix="/api/v1/auth/")
    