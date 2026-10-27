import os
from dotenv import load_dotenv
import smtplib
from email.message import EmailMessage


load_dotenv()

def send_email(to_email:str , subject:str , body:str):
    message = EmailMessage()
    message["From"] = os.getenv("EMAIL_USER")
    message["To"] = to_email
    message["Subject"] = subject
    message.set_content(body)

    with smtplib.SMTP(
        os.getenv("SMTP_HOST"),
        int(os.getenv("SMTP_PORT"))

    ) as server:
        server.starttls()
        server.login(
            os.getenv("EMAIL_USER"),
            os.getenv("EMAIL_PASS")
        )
        server.send_message(message)
        
send_email(
    to_email="anshmgy@gmail.com",
    subject="FastAPI Blog Email Test",
    body="Success! Your FastAPI Blogapp can send emails."
)

print("Email sent successfully!")
        