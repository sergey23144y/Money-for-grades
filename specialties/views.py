import requests
from rest_framework.viewsets import ModelViewSet

from specialties.models import Specialty, SpecialtyCategory
from specialties.serializers import SpecialtyViewSetSerializer


def get_specialties_from_hh():
    professional_roles_url = 'https://api.hh.ru/professional_roles'
    roles_request = requests.request('get', url=professional_roles_url)
    response_roles = roles_request.json()
    for category in response_roles['categories']:
        category_name = category['name']
        if not SpecialtyCategory.objects.filter(name=category_name).exists():
            specialty_category = SpecialtyCategory.objects.create(name=category_name)
        for role in category['roles']:
            name = role['name']
            if not Specialty.objects.filter(name=name).exists():
                specialty = Specialty.objects.create(
                    name=name,
                    category=SpecialtyCategory.objects.get(name=category_name)
                )


def get_number_for_specialties():
    professional_roles_url = 'https://api.hh.ru/professional_roles'
    roles_request = requests.request('get', url=professional_roles_url)
    response_roles = roles_request.json()
    for category in response_roles['categories']:
        for role in category['roles']:
            name = role['name']
            number = role['id']
            Specialty.objects.filter(name=name).update(number=number)


class SpecialtyViewSet(ModelViewSet):
    queryset = Specialty.objects.all()
    serializer_class = SpecialtyViewSetSerializer


class SpecialtyCategoriesViewSet(ModelViewSet):
    queryset = SpecialtyCategory.objects.all()
    serializer_class = SpecialtyViewSetSerializer
