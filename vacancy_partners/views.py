from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from vacancy_partners.models import VacancyPartner
from vacancy_partners.serializers import VacancyPartnerViewSetSerializer


class VacancyPartnerViewSet(ModelViewSet):
    queryset = VacancyPartner.objects.all()
    serializer_class = VacancyPartnerViewSetSerializer