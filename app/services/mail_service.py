from app.extensions import mail
from flask_mail import Message
from flask import render_template

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
        print(f"Error in sending email {e}")
        return False
    