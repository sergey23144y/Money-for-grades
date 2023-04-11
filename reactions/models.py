import uuid
from django.db import models
from users.models import User
from vacancy_partners.models import VacancyPartner


class ReactionsUsers(models.Model):
    types_of_reactions = [
        ('like', 'Нравится'),
        ('dislike', 'Не нравится'),
    ]
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateField(auto_now_add=True, blank=True, null=True, verbose_name='Дата')
    time = models.TimeField(auto_now_add=True, blank=True, null=True, verbose_name='Время')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name='Соискатель')
    vacancy_partner = models.ForeignKey(VacancyPartner, on_delete=models.CASCADE, null=True,
                                        verbose_name='Работодатель')
    reaction_type = models.CharField(max_length=7, choices=types_of_reactions, verbose_name="Реакция")

    def __str__(self):
        return f'{self.user} | {self.reaction_type} | {self.vacancy_partner}'

    class Meta:
        verbose_name = "Реакции соискателя"
        verbose_name_plural = "Реакции соискателей"
        ordering = ['-date', '-time']


class ReactionsEmployers(models.Model):
    types_of_reactions = [
        ('like', 'Нравится'),
        ('dislike', 'Не нравится'),
    ]
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateField(auto_now_add=True, blank=True, null=True, verbose_name='Дата')
    time = models.TimeField(auto_now_add=True, blank=True, null=True, verbose_name='Время')
    vacancy_partner = models.ForeignKey(VacancyPartner, on_delete=models.CASCADE, null=True,
                                        verbose_name='Работодатель')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name='Соискатель')
    reaction_type = models.CharField(max_length=7, choices=types_of_reactions, verbose_name="Реакция")

    def __str__(self):
        return f'{self.vacancy_partner} | {self.reaction_type} | {self.user}'

    class Meta:
        verbose_name = "Реакции работодателя"
        verbose_name_plural = "Реакции работодателей"
        ordering = ['-date', '-time']
