from app.extensions import mail
from flask_mail import Message
from flask import render_template
from app.extensions import logger

def send_otp_email(email, otp):
    """Sends the OTP email to the specified email address."""

    try:
        msg = Message(
            subject="OTP Verification",
            recipients=[email]
        )
        # msg.html = render_template("otp_template.html", otp=otp)
        # mail.send(msg)
        return True
    except Exception as e:
        logger.error(f"Error in sending email {e}")
        return False


def send_reminder_email(event, user):
    """Sends the OTP email to the specified email address."""

    msg = Message(
        subject=f"Reminder: {event.title} is coming up soon!",
        recipients=[user.email]
    )
    msg.html = render_template("reminder_template.html", user_name=user.name, event_title=event.title, event_date= str(event.event_date))
    
    try:
        mail.send(msg)
        logger.info(f"Reminder sent for event {event.id} to {user.email}")
        return True
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False
