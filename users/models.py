from uuid import uuid4

from authemail.models import EmailAbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import Group
from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField

from courses.models import PersonalityType
from django_back_api.utils import convert_image, rename_image
from skills.models import Skill
from specialties.models import Specialty, SpecialtyCategory
from study_partners.models import StudyPartner
from vacancies.models import Vacancy


class UserType(models.Model):
    name = models.CharField(max_length=32, blank=True)

    def __str__(self):
        return self.name


class SalesFunnel(models.Model):
    name = models.CharField(max_length=32, blank=True)

    def __str__(self):
        return self.name


class SalesChannel(models.Model):
    name = models.CharField(max_length=32, blank=True)

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=128, blank=True)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=128, blank=True)

    def __str__(self):
        return self.name


class School(models.Model):
    name = models.CharField(max_length=128, blank=True)

    def __str__(self):
        return self.name


class SecondaryEducation(models.Model):
    name = models.CharField(max_length=128, blank=True)

    def __str__(self):
        return self.name


class University(models.Model):
    name = models.CharField(max_length=128, blank=True)

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(max_length=128, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Язык"
        verbose_name_plural = "Языки"


class EmailUserManager(BaseUserManager):
    def _create_user(self, email, password, is_staff, is_superuser,
                     is_verified, **extra_fields):
        """
        Creates and saves a User with a given email and password.
        """
        now = timezone.now()
        register_group = Group.objects.filter(name='registered')
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, is_verified=is_verified,
                          last_login=now, date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        user.groups.set(register_group)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True, True,
                                 **extra_fields)


def user_directory_avatar_path(instance, filename):
    png_filename = rename_image(filename)
    return f"user_avatars/{instance.uid}/{png_filename}"


class User(EmailAbstractUser):
    work_experience_in_years = [
        ('0', 'Менее года'),
        ('1', '1 год'),
        ('2', '2 года'),
        ('3', '3 года'),
        ('4', '4 года'),
        ('5', '5 лет'),
        ('6', 'Более 6 лет'),
    ]
    ranks_of_professionalism = [
        ('beginner', 'Начинающий'),
        ('average', 'Средний'),
        ('professional', 'Профессионал'),
    ]
    uid = models.UUIDField(primary_key=True, default=uuid4)
    avatar = models.ImageField(upload_to=user_directory_avatar_path, null=True, blank=True, verbose_name='Аватар')
    rate = models.DecimalField(default=0, max_digits=8, decimal_places=2,
                               verbose_name='Ставка согласно "Оценке навыков"')
    current_rate = models.DecimalField(default=0, max_digits=8, decimal_places=2, verbose_name='Текущая ставка в час')
    middle_name = models.CharField(max_length=30, blank=True, verbose_name='Отчество')
    birthday = models.DateField(blank=True, null=True, verbose_name='День рождения')
    specialty_category = models.ForeignKey(SpecialtyCategory, on_delete=models.SET_NULL, null=True,
                                           verbose_name='Категория специальности')
    specialties = models.ForeignKey(Specialty, on_delete=models.SET_NULL, null=True, verbose_name='Специальность')
    user_type = models.ForeignKey(UserType, on_delete=models.SET_NULL, null=True)
    comment = models.TextField(blank=True)
    telegram = models.CharField(max_length=128, blank=True)
    study_partners = models.ForeignKey(StudyPartner, on_delete=models.SET_NULL, null=True)
    personality_type = models.ForeignKey(PersonalityType, on_delete=models.SET_NULL, null=True,
                                         verbose_name='Тип личности', blank=True)
    sales_funnel = models.ForeignKey(SalesFunnel, on_delete=models.SET_NULL, null=True)
    sales_channel = models.ForeignKey(SalesChannel, on_delete=models.SET_NULL, null=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    cover = models.ImageField(upload_to='users_images/', null=True)
    bonus_account = models.IntegerField(default=0)
    vacancy = models.ForeignKey(Vacancy, on_delete=models.SET_NULL, null=True)
    phone = PhoneNumberField(blank=True, verbose_name='Телефон')
    school = models.ForeignKey(School, on_delete=models.SET_NULL, null=True)
    secondary_education = models.ForeignKey(SecondaryEducation, on_delete=models.SET_NULL, null=True)
    university = models.ForeignKey(University, on_delete=models.SET_NULL, null=True)
    experience = models.CharField(max_length=1, verbose_name="Опыт работы",
                                  choices=work_experience_in_years, blank=True)
    level_of_professionalism = models.CharField(max_length=12, blank=True,
                                                verbose_name="Уровень профессионализма",
                                                choices=ranks_of_professionalism)
    languages = models.ManyToManyField(Language, blank=True, verbose_name='Языки')
    about_yourself = models.TextField(max_length=500, blank=True, verbose_name="О себе")
    objects = EmailUserManager()
    vocational_education = models.BooleanField(default=False, help_text='Среднее специальное образование',
                                               verbose_name='ССО')
    higher_education = models.BooleanField(default=False, help_text='Высшее образование', verbose_name='ВО')
    second_higher_education = models.BooleanField(default=False, help_text='Второе высшее образование',
                                                  verbose_name='ВВО')
    additional_education = models.BooleanField(default=False, help_text='Дополнительное профессиональное образование',
                                               verbose_name='ДПО')
    skills = models.ManyToManyField(Skill, blank=True, verbose_name='Навыки')
    money_for_grades = models.IntegerField(default=0, verbose_name='Бонус "Деньги за оценки"', blank=True)
    publication = models.BooleanField(default=False, verbose_name='Публикация')

    def rating(self):
        queryset = User.objects.filter(specialties=self.specialties).order_by('-current_rate')
        if self.specialties is not None:
            if self.current_rate != 0:
                for index, item in enumerate(queryset):
                    if self.email == item.email:
                        return index + 1
            else:
                return 'Не указана текущая ставка в час'
        else:
            return 'Не указана специальность'

    rating.allow_tags = False
    rating.short_description = 'Рейтинг'

    def __str__(self):
        return f'{self.email}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.avatar:
            convert_image(self.avatar, 500, 500)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        permissions = [('can_moderate_tasks', 'Can moderate tasks'), ]


class UserVKId(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    vk_id = models.IntegerField()


class UserSkill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, null=True)
    level = models.IntegerField(default=0)


class UserRateHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    rate = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
