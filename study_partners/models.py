from datetime import datetime

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from study_partners.fields import CodeField
from teachers.models import Teacher


class StudyPartner(models.Model):
    name = models.CharField(max_length=256, blank=True)
    description = models.TextField(blank=True)
    title = models.CharField(max_length=256, blank=True)
    definition = models.TextField(blank=True)
    is_parsed = models.BooleanField(blank=True)
    image = models.ImageField(upload_to='logo', blank=True, null=True)
    certificate = models.ImageField(upload_to='course_certificates', blank=True, null=True)
    found_year = models.PositiveIntegerField(
        validators=[MinValueValidator(1900), MaxValueValidator(datetime.now().year)],
        help_text="Нужно использовать число от 1900 до настоящего года в четырехзначном формате",
        null=True,
        blank=True
    )
    course_quantity = models.PositiveIntegerField(default=0, blank=True)
    code = CodeField(null=True, blank=True)
    telegram_id = models.BigIntegerField(null=True, blank=True)
    rating = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        help_text="Число должно быть от 0 до 5",
        blank=True
    )
    teachers = models.ManyToManyField(Teacher, blank=True)
    applications = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Онлайн-школа/ВУЗ"
        verbose_name_plural = "Онлайн-школы/ВУЗы"