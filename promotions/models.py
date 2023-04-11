from django.db import models

from study_partners.models import StudyPartner
from vacancy_partners.models import VacancyPartner


class PromotionCitiesCategories(models.Model):
    name = models.CharField(max_length=64, blank=True)


class Promotion(models.Model):
    name = models.CharField(max_length=256, blank=True, verbose_name='Название')
    title = models.CharField(max_length=256, blank=True, verbose_name='Заголовок')
    definition = models.TextField(blank=True, null=True, verbose_name='Определение')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    image = models.ImageField(upload_to='image', blank=True, null=True, verbose_name='Изображение')
    coupon = models.CharField(max_length=256, blank=True, verbose_name='Купон')
    link = models.URLField(blank=True, verbose_name='Ссылка')
    cities = models.ManyToManyField(PromotionCitiesCategories, blank=True, verbose_name='Города')
    vacancy_partner = models.ForeignKey(VacancyPartner, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Работодатель')
    study_partner = models.ForeignKey(StudyPartner, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Онлайн-школа/ВУЗ')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Акция"
        verbose_name_plural = "Акции"
