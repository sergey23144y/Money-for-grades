import uuid

from django.db import models
from users.models import User
from study_partners.models import StudyPartner


class Order(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateField(auto_now_add=True, blank=True, null=True)
    time = models.TimeField(auto_now_add=True, blank=True, null=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    study_partner = models.ForeignKey(StudyPartner, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.user_id.email

    class Meta:
        verbose_name = "Заявка пользователей"
        verbose_name_plural = "Заявки пользователей"
