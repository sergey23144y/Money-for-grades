import uuid

from django.db import models

from courses.models import Course, PersonalityType
from skills.models import Skill
from vacancy_partners.models import VacancyPartner


class VacancyCategory(models.Model):
    name = models.CharField(max_length=128, blank=True)
    image = models.ImageField(upload_to='vacancy_categories_images', blank=True, null=True)
    title = models.CharField(max_length=128, blank=True)
    definition = models.CharField(max_length=256, blank=True)
    description = models.CharField(max_length=256, blank=True)
    base_category = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


class TypeOfWork(models.Model):
    name = models.CharField(max_length=16, blank=True)

    def __str__(self):
        return self.name


class WorkSchedule(models.Model):
    name = models.CharField(max_length=16, blank=True)

    def __str__(self):
        return self.name


class Vacancy(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vacancy_category = models.ForeignKey(VacancyCategory, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=128, blank=True)
    summary = models.CharField(max_length=256, blank=True)
    title = models.CharField(max_length=128, blank=True)
    definition = models.CharField(max_length=256, blank=True)
    description = models.TextField(blank=True)
    image_mini = models.ImageField(upload_to='course_images', blank=True, null=True)
    image = models.ImageField(upload_to='course_images', blank=True, null=True)
    image_mobile = models.ImageField(upload_to='course_images', blank=True, null=True)
    payment = models.CharField(max_length=128, blank=True)
    internship = models.CharField(max_length=128, blank=True)
    type_of_work = models.ForeignKey(TypeOfWork, on_delete=models.CASCADE, null=True)
    vacancy_partner = models.ForeignKey(VacancyPartner, on_delete=models.CASCADE, null=True)
    courses = models.ManyToManyField(Course, blank=True)
    work_schedule = models.ForeignKey(WorkSchedule, on_delete=models.CASCADE, null=True)
    link = models.URLField(blank=True)
    personality_type = models.ForeignKey(PersonalityType, on_delete=models.CASCADE, null=True)


class VacancyRequirement(models.Model):
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, null=True)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, null=True)
    level = models.IntegerField(default=0)