from fastapi_mail import ConnectionConfig,MessageSchema,FastMail
from app.core.config import settings
from app.services.celery_app import app
import asyncio
conf = ConnectionConfig(
    
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD = settings.MAIL_PASSWORD,
    MAIL_FROM = settings.MAIL_FROM,
    MAIL_PORT = settings.MAIL_PORT,
    MAIL_SERVER = settings.MAIL_SERVER,
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True
                       ) 

fm=FastMail(conf)
@app.task
def send_verification_email(tokenn:str,email:str):
    message = MessageSchema(
    subject="Verify your email",
    recipients=[email],
    body=f"""
    <p>Hi,</p>

    <p>Please click the link below to verify your email:</p>

    <p>
        <a href="http://localhost:8000/auth/verify?token={tokenn}">
            Verify Email
        </a>
    </p>

    <p>If you did not sign up, you can ignore this email.</p>
    """,
    subtype="html"
)
    asyncio.run(fm.send_message(message))
