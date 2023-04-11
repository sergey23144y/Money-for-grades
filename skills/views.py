from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from skills.models import Skill
from skills.serializers import SkillModelSerializer


# Create your views here.
class SkillViewSet(ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillModelSerializer

