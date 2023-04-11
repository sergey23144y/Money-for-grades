import json
import environ
from django.core.management.base import BaseCommand
from courses.models import CourseSubcategory
from faker import Faker

fake = Faker()

env = environ.Env()
environ.Env.read_env()


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('django_back_api/jsons/course_base_categories.json', 'r', encoding='utf-8') as db_data:
            data = json.loads(db_data.read())
        categories = [CourseSubcategory(name=category.get('name')) for category in data]
        CourseSubcategory.objects.bulk_create(categories)

