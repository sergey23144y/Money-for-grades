import json
from django.core.management import BaseCommand
from courses.models import PayType, TypeOfLearning, Payment, TypeOfTraining, CourseOrigin, Status


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('django_back_api/jsons/db_data.json', 'r', encoding='utf-8') as db_data:
            data = json.loads(db_data.read())

        type_of_training = TypeOfTraining.objects.all()
        type_of_training.delete()
        for training_type in data['type_of_training']:
            type_of_training = TypeOfTraining.objects.create(name=training_type)
            type_of_training.save()

        type_of_learning = TypeOfLearning.objects.all()
        type_of_learning.delete()
        for learning_type in data['type_of_learning']:
            type_of_training = TypeOfLearning.objects.create(name=learning_type)
            type_of_training.save()

        course_origins = CourseOrigin.objects.all()
        course_origins.delete()
        for course_origin in data['course_origin']:
            course_orig = CourseOrigin.objects.create(name=course_origin)
            course_orig.save()

        statuses = Status.objects.all()
        statuses.delete()
        for status in data['status']:
            stat = Status.objects.create(name=status)
            stat.save()


