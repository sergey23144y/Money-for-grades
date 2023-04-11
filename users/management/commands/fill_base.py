import json
from django.contrib.auth.models import Group, Permission
from django.core.management import BaseCommand
from django.db.models import Q
from courses.models import PayType, TypeOfLearning, Payment
from promotions.models import PromotionCitiesCategories
from skills.models import SkillCategory
from study_partners.models import StudyPartner
from vacancies.models import TypeOfWork, WorkSchedule


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('django_back_api/jsons/db_data.json', 'r', encoding='utf-8') as db_data:
            data = json.loads(db_data.read())

        with open('django_back_api/jsons/study_partners.json', 'r', encoding='utf-8') as db_data:
            study_partners_file = json.loads(db_data.read())

        user_groups = Group.objects.all()
        user_groups.delete()
        user_group = Group.objects.create(name='administrator')
        user_group.save()
        perm = Permission.objects.all()
        user_group.permissions.set([*perm])
        user_group = Group.objects.create(name='tutor')
        user_group.save()
        perms = Permission.objects.filter(Q(name__contains='view') | Q(name__contains='add') | Q(name__contains='log entry'))
        user_group.permissions.set([*perms])
        user_group = Group.objects.create(name='operator')
        user_group.save()
        perms = Permission.objects.filter(
            Q(name__contains='view') |
            Q(name__contains='add') |
            Q(name__contains='log entry') |
            Q(name__contains='change')
        )
        user_group.permissions.set([*perms])
        user_group = Group.objects.create(name='registered')
        user_group.save()
        # perms = Permission.objects.filter(
        #     Q(name='Can add user') |
        #     Q(name='Can change user') |
        #     Q(name='Can delete user') |
        #     Q(name='Can view user')
        #     )
        # user_group.permissions.set([*perms])

        cities = PromotionCitiesCategories.objects.all()
        cities.delete()

        for region in data['regions']:
            city = PromotionCitiesCategories.objects.create(name=region)
            city.save()

        pay_types = PayType.objects.all()
        pay_types.delete()
        for pay_type in data['pay_types']:
            pay_type_db = PayType.objects.create(name=pay_type)
            pay_type_db.save()

        type_of_learning = TypeOfLearning.objects.all()
        type_of_learning.delete()
        for learning_type in data['type_of_learning']:
            type_of_training = TypeOfLearning.objects.create(name=learning_type)
            type_of_training.save()

        payment = Payment.objects.all()
        payment.delete()
        for pay in data['payment']:
            payment = Payment.objects.create(name=pay)
            payment.save()

        type_of_work = TypeOfWork.objects.all()
        type_of_work.delete()
        for work_type in data['type_of_work']:
            type_of_work = TypeOfWork.objects.create(name=work_type)
            type_of_work.save()

        work_schedule = WorkSchedule.objects.all()
        work_schedule.delete()
        for schedule_of_work in data['work_schedule']:
            work_schedule = WorkSchedule.objects.create(name=schedule_of_work)
            work_schedule.save()

        skill_categories = SkillCategory.objects.all()
        skill_categories.delete()
        for skill_category in data['skill_categories']:
            skill_cat = SkillCategory.objects.create(name=skill_category)
            skill_cat.save()

        study_par = StudyPartner.objects.all()
        study_par.delete()
        for partner in study_partners_file:
            StudyPartner.objects.create(name=partner, is_parsed=False).save()
