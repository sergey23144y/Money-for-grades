import json
from random import randint, choice, choices

import environ
from django.core.management.base import BaseCommand

from ads.models import Advertisement
from courses.models import Book, CourseCategory, Software, StudyProgram, PersonalityType, Course, TypeOfLearning, Status
from skills.models import Skill, SkillCategory
from specialties.models import Specialty
from teachers.models import Teacher
from users.models import User
from faker import Faker
from study_partners.models import StudyPartner
from vacancies.models import VacancyCategory, Vacancy, WorkSchedule, VacancyRequirement
from vacancy_partners.models import VacancyPartner
from promotions.models import Promotion
from promotions.models import PromotionCitiesCategories

fake = Faker()

env = environ.Env()
environ.Env.read_env()


class Command(BaseCommand):
    def handle(self, *args, **options):
        courses = [
            {
                "name": "КАК ОТКРЫТЬ ПРИБЫЛЬНУЮ КЛИНИКУ Пошаговый план действий",
                "definition": "https://medicalbusinesschool.com/klinika#reg",
                "description": "https://medicalbusinesschool.com/klinika#reg",
                "duration_of_training": "1 месяц",
                "course_start": "2023-01-24"
            },
            {
                "name": "Навыки общения врача с пациентами. Увеличиваем продажи в клинике",
                "definition": "https://medicalbusinesschool.com/navyki-obshcheniya",
                "description": "https://medicalbusinesschool.com/navyki-obshcheniya",
                "duration_of_training": "1 месяц",
                "course_start": "2023-01-23"
            },
            {
                "name": "КАК СТАТЬ ЭФФЕКТИВНЫМ АДМИНИСТРАТОРОМ РЕГИСТРАТУРЫ И ОПЕРАТОРОМ КОНТАКТ ЦЕНТРА",
                "definition": "https://medicalbusinesschool.com/effective-administration",
                "description": "https://medicalbusinesschool.com/effective-administration",
                "duration_of_training": "2 нед",
                "course_start": "2023-01-16"
            },
            {
                "name": "РЕГИСТРАТУРА И КОНТАКТ ЦЕНТР КЛИНИКИ",
                "definition": "https://medicalbusinesschool.com/contact-center",
                "description": "https://medicalbusinesschool.com/contact-center",
                "duration_of_training": "2 нед ",
                "course_start": "2023-01-16"
            },
            {
                "name": "ФИНАНСОВОЕ ПЛАНИРОВАНИЕ ДЛЯ ЧАСТНОЙ КЛИНИКИ",
                "definition": "https://medicalbusinesschool.com/finansy",
                "description": "https://medicalbusinesschool.com/finansy",
                "duration_of_training": "2 мес",
                "course_start": "2023-03-13"
            }
        ]
        study_partner = StudyPartner.objects.get(name='medicalbusinesschool.com')
        type_of_learning = TypeOfLearning.objects.get(name='онлайн')
        print(study_partner, type_of_learning)
        for i in courses:
            course = Course.objects.create(
                name=i.get('name'),
                definition=i.get('definition'),
                description=i.get('description'),
                duration_of_training=i.get('duration_of_training'),
                is_active=True,
                course_start=i.get('course_start'),
                type_of_learning=type_of_learning,
                study_partner=study_partner
            )

            course.save()
