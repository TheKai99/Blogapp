from src.utils.email_utils import send_email


send_email(
    to_email="anshmgy@gmail.com",
    subject="FastAPI Blog Email Test",
    body="Success! Your FastAPI Blogapp can send emails."
)

print("Email sent successfully!")