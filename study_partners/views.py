from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from study_partners.models import StudyPartner
from study_partners.serializers import StudyPartnerViewSetSerializer


class StudyPartnerViewSet(ModelViewSet):
    queryset = StudyPartner.objects.all()
    serializer_class = StudyPartnerViewSetSerializer