from smtplib import SMTPException
from ingenium.celery import app
from .services import UserService, VerifyMailingService


@app.task(bind=True, max_retries=3)
def send_verification_email_task(self, user_id: int) -> None: 
    try:
        VerifyMailingService.send_verification_email(user_id)
    except SMTPException as ex: 
        raise self.retry(exc=ex, countdown=5)  
    
@app.task 
def delete_inactive_user_task() -> None: 
    UserService.delete_all_inactive_users()