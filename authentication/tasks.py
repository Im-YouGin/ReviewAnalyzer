from celery import shared_task
from django.contrib.auth import get_user_model

from config import settings


@shared_task
def q_email_user(user_id, subject, email):
    User = get_user_model()
    user = User.objects.filter(id=user_id).first()

    if not user:
        return

    user.email_user(subject, email)
