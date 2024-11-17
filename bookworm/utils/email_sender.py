from django.core.mail import EmailMessage

from bookworm.settings import EMAIL_HOST_USER
from logger.log import logger


def send_single_email(
        subject: str,
        message: str,
        send_to: str,
        file=None,
        send_from: str = EMAIL_HOST_USER,
) -> bool:
    """Email send handler."""
    logger.info("Received a request to send a email")
    logger.info(
        f"Received data:"
        f"{subject=}"
        f"{message=}"
        f"{send_from=}"
        f"{send_to=}"
    )
    try:
        email = EmailMessage(
            subject,
            message,
            send_from,
            [send_to],
        )
        if file:
            email.attach(file.name, file.read(), file.content_type)
        email.send(fail_silently=False)
        logger.info(f"Email sent successfully to {send_to}")
    except Exception as er:
        logger.error(f"Error sending email: {er}")
        return False
    return True
