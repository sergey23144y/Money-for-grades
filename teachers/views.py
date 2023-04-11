from rest_framework.viewsets import ModelViewSet

from teachers.models import Teacher
from teachers.serializers import TeacherViewSetSerializer


class TeacherViewSet(ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherViewSetSerializer
