from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_mail import Mail
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from apscheduler.schedulers.background import BackgroundScheduler
import logging

db = SQLAlchemy()
migrate = Migrate() 
jwt = JWTManager()
mail = Mail()
limiter = Limiter(key_func=get_remote_address)
scheduler = BackgroundScheduler()


# Logging setup
def setup_logging():
    logging.basicConfig(level=logging.INFO)  # Set the log level to INFO or DEBUG for detailed logs
    logger = logging.getLogger(__name__)
    return logger

logger = setup_logging()