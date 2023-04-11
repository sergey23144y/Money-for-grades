from django.db import models

from skills.models import Skill


class SpecialtyCategory(models.Model):
    name = models.CharField(max_length=256, blank=True, verbose_name='Категория специализации')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория специализаций'
        verbose_name_plural = 'Категории специализаций'
        ordering = ['name']


class Specialty(models.Model):
    name = models.CharField(max_length=256, blank=True, verbose_name='Специализация')
    category = models.ForeignKey(SpecialtyCategory, on_delete=models.SET_NULL, null=True,
                                 verbose_name='Категория специализации')
    number = models.IntegerField(default=0, verbose_name='id')
    minimum_rate = models.DecimalField(default=0, max_digits=8, decimal_places=2, verbose_name='Минимальная ставка')
    average_rate = models.DecimalField(default=0, max_digits=8, decimal_places=2, verbose_name='Средняя ставка')
    maximum_rate = models.DecimalField(default=0, max_digits=8, decimal_places=2, verbose_name='Максимальная ставка')
    key_skills = models.ManyToManyField(Skill, blank=True, verbose_name='Ключевые навыки')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Специализация'
        verbose_name_plural = 'Специализации'
        ordering = ['name']
