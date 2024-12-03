from flask import Flask
from flask_mail import Mail, Message
from datetime import datetime

app = Flask(__name__)

# Configure Flask-Mail to use MailHog
app.config.update(
    MAIL_SERVER='localhost',
    MAIL_PORT=2025,
    MAIL_USE_TLS=False,
    MAIL_USE_SSL=False,
    MAIL_DEFAULT_SENDER='test@householdservices.com'
)

mail = Mail(app)

def send_test_email():
    with app.app_context():
        try:
            msg = Message(
                subject='Test Email from Household Services',
                recipients=['test@example.com'],
                html=f"""
                <h1>Test Email</h1>
                <p>This is a test email sent at {datetime.now()}</p>
                <p>If you're seeing this, your MailHog setup is working correctly!</p>
                """
            )
            mail.send(msg)
            print("✅ Test email sent successfully!")
            print("📧 Check MailHog at http://localhost:8025")
        except Exception as e:
            print(f"❌ Error sending email: {str(e)}")

if __name__ == "__main__":
    send_test_email() 