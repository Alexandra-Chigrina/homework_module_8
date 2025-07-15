from dateutil.relativedelta import relativedelta

from celery import shared_task
from django.utils import timezone

from users.models import User


@shared_task
def deactivate_inactive_user():
    """Блокирует пользователей, которые не заходили в аккаунт более 30 дней."""
    one_month_ago = timezone.now() - relativedelta(months=1)
    user_to_deactivate = User.objects.filter(is_active=True, last_login__lt=one_month_ago)

    count = user_to_deactivate.update(is_active=False)

    return f"Deactivated {count} users"
