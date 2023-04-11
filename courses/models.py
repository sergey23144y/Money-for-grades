import uuid

from autoslug import AutoSlugField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from courses.fields import VendorCodeField
from django_back_api.utils import rename_image, convert_image
from skills.models import Skill
# from specialties.models import Specialty
from study_partners.models import StudyPartner
from teachers.models import Teacher
# from users.models import User
from webmaster.models import WebmasterCategory


class CourseSubcategory(models.Model):
    name = models.CharField(max_length=128, blank=True)
    image = models.ImageField(upload_to='course_categories_images', blank=True, null=True)
    title = models.CharField(max_length=128, blank=True)
    definition = models.CharField(max_length=256, blank=True)
    description = models.CharField(max_length=256, blank=True)
    slag = AutoSlugField(populate_from='name', unique=True, null=True)
    base_category = models.ForeignKey('CourseCategory', on_delete=models.SET_NULL, null=True)
    seo = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Подкатегория курса"
        verbose_name_plural = "Подкатегории курсов"


class CourseCategory(models.Model):
    name = models.CharField(max_length=128, blank=True)
    image = models.ImageField(upload_to='course_categories_images', blank=True, null=True)
    title = models.CharField(max_length=128, blank=True)
    definition = models.CharField(max_length=256, blank=True)
    description = models.CharField(max_length=256, blank=True)
    slag = AutoSlugField(populate_from='name', unique=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория курса"
        verbose_name_plural = "Категории курсов"


class PayType(models.Model):
    name = models.CharField(max_length=16, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Мера времени оплаты"
        verbose_name_plural = "Меры времени оплаты"


class TypeOfLearning(models.Model):
    name = models.CharField(max_length=16, blank=True)

    def __str__(self):
        return self.name


class Payment(models.Model):
    name = models.CharField(max_length=8, blank=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    name = models.CharField(max_length=32, blank=True)

    def __str__(self):
        return self.name


class Software(models.Model):
    name = models.CharField(max_length=32, blank=True)

    def __str__(self):
        return self.name


class StudyProgram(models.Model):
    name = models.CharField(max_length=32, blank=True)

    def __str__(self):
        return self.name


class PersonalityType(models.Model):
    name = models.CharField(max_length=32, blank=True)

    def __str__(self):
        return self.name


class TypeOfTraining(models.Model):
    name = models.CharField(max_length=32, blank=True)

    def __str__(self):
        return self.name


class CourseOrigin(models.Model):
    name = models.CharField(max_length=32, blank=True)

    def __str__(self):
        return self.name


class Status(models.Model):
    name = models.CharField(max_length=32, blank=True)

    def __str__(self):
        return self.name


class CourseProgram(models.Model):
    name = models.CharField(max_length=256, blank=True)

    def __str__(self):
        return self.name


def course_directory_avatar_path(instance, filename):
    png_filename = rename_image(filename)
    return f"course_images/{instance.uid}/{png_filename}"


class Course(models.Model):
    def get_seo_description(self):
        return f"{self.name} - выбирайте подходящий вариант через Sokrat. Вы сможете получить новые навыки и освоить профессию с нуля, обучаясь дистанционно."

    def get_seo_title(self):
        return f"{self.name} - записаться через Sokrat"

    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vendor = VendorCodeField(null=True, max_length=8, unique=True, editable=False)
    slag = AutoSlugField(max_length=256, populate_from='name', unique=True, null=True)
    course_category = models.ManyToManyField(CourseCategory, verbose_name="Подкатегория курса", help_text="Можно выбрать больше одной категории", blank=True)
    course_sub_category = models.ManyToManyField(CourseSubcategory, verbose_name="Категория курса", help_text="Можно выбрать больше одной категории", blank=True)
    name = models.CharField(max_length=256, blank=True, verbose_name="Название курса")
    summary = models.TextField(max_length=256, blank=True, verbose_name="Описание курса")
    title = models.CharField(max_length=128, blank=True, verbose_name="Заголовок", default=get_seo_title)
    description = models.TextField(blank=True, help_text="Заполняется автоматически(SEO)", verbose_name="Описание", default=get_seo_description)
    last_price = models.PositiveIntegerField(null=True, blank=True, verbose_name="Последняя цена")
    currency_symbol = models.CharField(max_length=1, default="₽", verbose_name="Валюта", choices=(('₽', '₽'), ('€', '€'), ('$', '$')))
    pay_type = models.ForeignKey(PayType, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Тип цены")
    #!!не понял что поменять
    study_partner = models.ForeignKey(StudyPartner, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Партнер")
    rating = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        help_text="Число должно быть от 0 до 5",
        verbose_name="Рейтинг"
    )
    image_mini = models.ImageField(upload_to=course_directory_avatar_path, blank=True, null=True, verbose_name="Картинка миниатюра")
    image = models.ImageField(upload_to=course_directory_avatar_path, blank=True, null=True, verbose_name="Картинка WEB")
    image_mobile = models.ImageField(upload_to=course_directory_avatar_path, blank=True, null=True, verbose_name="Картинка мобильная")
    certificate = models.ImageField(upload_to='course_certificates', blank=True, null=True, verbose_name="Сертификат")
    teachers = models.ManyToManyField(Teacher, blank=True, verbose_name="Учителя")
    type_of_learning = models.ForeignKey(TypeOfLearning, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Тип обучения")
    study_program = models.ManyToManyField(StudyProgram, verbose_name="Программа курса", blank=True)
    duration_of_training = models.CharField(max_length=256, blank=True, verbose_name="Продолжительность курса", help_text="Только цифры")
    support_url = models.URLField(default='https://sokratinvest.ru/supportsokrat', null=True, verbose_name="Кнопка бесплатная консультация")
    course_origin = models.ForeignKey(CourseOrigin, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Источник курса")
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True, default=4, verbose_name="Статус курса")
    type_of_training = models.ForeignKey(TypeOfTraining, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Значение продолжительности курса")
    updated_at = models.DateField(auto_now=True, null=True)
    course_start = models.DateField(blank=True, null=True, verbose_name="Начало курса")
    course_start_time = models.TimeField(blank=True, null=True, verbose_name="Таймер")
    skills = models.ManyToManyField(Skill, verbose_name="Навыки", blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            convert_image(self.image, 2000, 2000)
        if self.image_mini:
            convert_image(self.image_mini, 700, 700)
        if self.image_mobile:
            convert_image(self.image_mobile, 400, 400)

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class CoursePrice(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    price = models.PositiveIntegerField(null=True)

    def __str__(self):
        return f'{self.course} - {self.price} - {self.date}'

    class Meta:
        verbose_name = "Архивная цена курса"
        verbose_name_plural = "Архивные цены курсов"


class CourseSkillLevelWeight(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, null=True)
    level_weight = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.course} - {self.skill} - {self.level_weight}'


class CourseCommit(models.Model):
    courses = models.ManyToManyField(Course, blank=True)
    name = models.CharField(max_length=256, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Подборка курсов"
        verbose_name_plural = "Поборки курсов"