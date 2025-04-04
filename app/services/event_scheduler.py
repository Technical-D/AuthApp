from datetime import datetime, timedelta
from app.models import Event, User
from app.extensions import db
from app.extensions import scheduler, logger
from app.services.mail_service import send_reminder_email
from apscheduler.triggers.interval import IntervalTrigger

reminder_lock = {}

def send_event_reminders(app):
    with app.app_context():
        global reminder_lock
        try:
            now = datetime.now()
            logger.info(f"Checking for upcoming events at {now}")
            upcoming_events = db.session.query(Event).filter(
                Event.event_date <= now + timedelta(hours=1),
                Event.event_date >= now,
                Event.reminded == False
            ).all()
            logger.info(f"Event detail: Found {len(upcoming_events)} Ids:{upcoming_events}")

            for event in upcoming_events:
                if event.id in reminder_lock:
                    logger.info(f"Skipping duplicate reminder for event {event.id}")
                    continue

                user = db.session.query(User).get(event.user_id)
                if user:
                    if send_reminder_email(event, user):
                        logger.info(f"Reminder sent for event {event.id} to {user.email}")
                        event.reminded = True
                        db.session.commit()
                        reminder_lock[event.id] = True
                        logger.info(f"Reminder sent for event {event.id} to {user.email}")
                    else:
                        logger.error(f"Failed to send reminder for event {event.id}")
                        db.session.rollback()
                            
        except Exception as e:
            logger.error(f"Error in sending reminders: {str(e)}")
            db.session.rollback()

def schedule_reminder_task(app):
    if not scheduler.get_job('reminder_task'):
        logger.info("Scheduling reminder job...")
        scheduler.add_job(
            func= lambda: send_event_reminders(app),  
            trigger=IntervalTrigger(minutes=2),  
            id='reminder_task',  
            replace_existing=True,
            max_instances=1
        )
