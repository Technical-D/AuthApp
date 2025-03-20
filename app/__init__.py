from flask import Flask
from app.extensions import db, migrate, jwt, mail, limiter
from app.error_handlers import handle_ratelimit_error
from app.routes import register_blueprints
from config import config_options
import os

def create_app():
    app = Flask(__name__)

    # Load Configuration
    env = os.getenv("FLASK_ENV", "development")
    app.config.from_object(config_options[env])

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    limiter.init_app(app)

    # Register Blueprints
    register_blueprints(app)

    # Registering error handler
    handle_ratelimit_error(app)

    return app