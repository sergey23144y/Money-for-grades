from celery import shared_task
from django.utils import timezone

from users.models import User, UserRateHistory


@shared_task(name="rate_history")
def rate_history():
    users = User.objects.all()
    users_list = [UserRateHistory(user=user, rate=user.rate, date=timezone.now()) for user in users]
    UserRateHistory.objects.bulk_create(users_list)