from flask import Flask
from app.extensions import db, migrate, jwt, mail, limiter, scheduler
from app.error_handlers import handle_ratelimit_error
from app.routes import register_blueprints
from config import config_options
import os
from flask_cors import CORS

def create_app():
    app = Flask(__name__)

    CORS(app)

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

    # registering the tasks
    from app.services.event_scheduler import schedule_reminder_task
    with app.app_context():
        if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
            schedule_reminder_task(app)
            scheduler.start()

    # Registering error handler
    handle_ratelimit_error(app)

    return app