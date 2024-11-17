import logging
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config import settings
from retry import retry


class SendEmailFailure(Exception):
    """
    Raise email not sent
    """

    pass


server = None


def create_connection():
    global server
    sender_email = settings.mail_username
    if server:
        try:
            server.quit()
        except Exception:
            pass
        server = None
    context = ssl.create_default_context()
    if settings.mail_server == "smtp.gmail.com":
        server = smtplib.SMTP_SSL(
            settings.mail_server, settings.mail_port, context=context
        )
        server.login(sender_email, settings.mail_app_password)
    else:
        server = smtplib.SMTP(host=settings.mail_server, port=settings.mail_port)
        server.starttls(context=context)
        server.login(sender_email, settings.mail_app_password)


def close_connection():
    global server
    if server:
        try:
            server.quit()
        except Exception:
            pass
        server = None


@retry(Exception, tries=3)
def send_email(recipient: str, subject: str, message: str) -> None:
    """
    Send email with okta credentials to recipient

    :param recipient:
    :param subject:
    :param message:
    :return:
    """

    try:
        create_connection()
        global server
        logging.info(f"Send email to {recipient} with subject {subject} and message:")
        sender_email = settings.mail_username
        receiver_email = recipient
        msg = message
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = f"Autom8 <{sender_email}>"
        message["To"] = receiver_email
        part2 = MIMEText(msg, "html")
        message.attach(part2)
        server.sendmail(sender_email, receiver_email, message.as_string())
    except Exception as ex:
        logging.error(str(ex))
        logging.error(f"Send email to {recipient} failure.")
        create_connection()
        raise SendEmailFailure
