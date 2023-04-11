import json
import environ
from django.core.management.base import BaseCommand
from courses.models import CourseSubcategory, Course
from faker import Faker

from study_partners.models import StudyPartner

fake = Faker()

env = environ.Env()
environ.Env.read_env()


class Command(BaseCommand):
    def handle(self, *args, **options):
        courses = Course.objects.all()
        count = 0
        for i in courses:
            count += 1
            print(f'-{i.vendor}---{count}----{bool(i.slag)}')
            if not i.vendor:
                s_p = StudyPartner.objects.get(id=i.study_partner.id)
                print(i.uid,'---', s_p.id)
                i.delete()
                break
            i.save()
        # s_p = StudyPartner.objects.get(name='medicalbusinesschool.com')
        # courses = Course.objects.filter(study_partner=s_p)
        # for c in courses:
        #     print(c.slag, '---',c.vendor)