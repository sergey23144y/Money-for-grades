from xml.dom.minidom import parse
from django.core.management.base import BaseCommand
from webmaster.models import WebmasterCategory


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('django_back_api/xmls/education_rubricator.xml', 'r', encoding='utf-8') as db_data:
            data = parse(db_data).getElementsByTagName('category')
        category = [WebmasterCategory(id=category.attributes['id'].value, name=category.childNodes[0].data) for category in data]
        WebmasterCategory.objects.bulk_create(category)
