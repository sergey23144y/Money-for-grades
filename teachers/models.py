from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Teacher(models.Model):
    first_name = models.CharField(max_length=32, blank=True)
    middle_name = models.CharField(max_length=32, blank=True)
    last_name = models.CharField(max_length=32, blank=True)
    image = models.ImageField(upload_to='course_images', blank=True, null=True)
    title = models.CharField(max_length=128, blank=True)
    definition = models.CharField(max_length=256, blank=True)
    description = models.TextField(blank=True)
    experience = models.CharField(max_length=64, blank=True)
    position = models.CharField(max_length=64, blank=True)
    rating = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        help_text="Число должно быть от 0 до 5"
    )
    company_one = models.CharField(max_length=32, blank=True)
    company_two = models.CharField(max_length=32, blank=True)
    company_three = models.CharField(max_length=32, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.middle_name} {self.last_name}'

    class Meta:
        verbose_name = "Преподаватель"
        verbose_name_plural = "Преподаватели"
