import logging
from typing import Dict, Union

from celery import shared_task
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


@shared_task
def send_feedback_mail(message_form: Dict[str, Union[int, str]]) -> None:
    logger.info(f"Send message: '{message_form}'")
    model_user = get_user_model()
    user_obj = model_user.objects.get(pk=message_form["id_from"])
    fromUser = user_obj.username if user_obj.email else user_obj.email

    send_mail(
        message_form["topic"],  # subject (title)
        message_form["message"],  # message
        fromUser,  # send from
        ["anya141196@mail.ru"],  # send to
        fail_silently=False,
    )
    return None
