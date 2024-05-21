#src.services.email.py

"""
Email Service Module.

This module contains the configuration for the email service and the function
to send an email with a verification token.
"""

from pathlib import Path
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from fastapi_mail.errors import ConnectionErrors
from pydantic import EmailStr
from src.services.auth import auth_service
from src.conf.config import settings

# Email service configuration
conf = ConnectionConfig(
    MAIL_USERNAME=settings.mail_username,
    MAIL_PASSWORD=settings.mail_password,
    MAIL_FROM="Project_FastAPI@meta.ua", #EmailStr(settings.mail_from),
    MAIL_PORT=settings.mail_port,
    MAIL_SERVER=settings.mail_server,
    MAIL_FROM_NAME="Desired Name",
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=Path(__file__).parent / 'templates',
)


async def send_email(email: EmailStr, username: str, host: str):
    """
    Send an email with a verification token to the specified email address.

    :param email: The email address to send the verification token to.
    :type email: EmailStr
    :param username: The username associated with the email address.
    :type username: str
    :param host: The host URL for the application.
    :type host: str
    :raises ConnectionErrors: If there is an error connecting to the email server.
    """
    try:
        token_verification = auth_service.create_email_token({"sub": email})
        message = MessageSchema(
            subject="Confirm your email ",
            recipients=[email],
            template_body={"host": host, "username": username, "token": token_verification},
            subtype=MessageType.html
        )

        # Initialize FastMail with the configuration
        fm = FastMail(conf)
        
        # Send the email message using the defined template
        await fm.send_message(message, template_name="email_template.html")
    except ConnectionErrors as err:
        print(err)

