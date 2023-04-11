from rest_framework.serializers import ModelSerializer

from teachers.models import Teacher


class TeacherViewSetSerializer(ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'