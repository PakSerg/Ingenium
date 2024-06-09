from celery import shared_task
from .services import UserService, VerifyMailingService


@shared_task
def send_verification_email_task(user_id: int) -> None: 
    VerifyMailingService.send_verification_email(user_id)
