import json
from django.core.management import BaseCommand
from users.models import UserType, SalesFunnel


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('django_back_api/jsons/db_data.json', 'r', encoding='utf-8') as db_data:
            data = json.loads(db_data.read())

        user_types = UserType.objects.all()
        user_types.delete()
        for user_type in data['user_types']:
            us_type = UserType.objects.create(name=user_type)
            us_type.save()

        sales_funnels = SalesFunnel.objects.all()
        sales_funnels.delete()
        for sales_funnel in data['sales_funnels']:
            sales_fun = SalesFunnel.objects.create(name=sales_funnel)
            sales_fun.save()
