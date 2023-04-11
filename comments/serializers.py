from rest_framework.serializers import ModelSerializer

from comments.models import CommentCourse, CommentTeacher, CommentStudyPartner


# Serializers for Admin, User
class CommentCourseSerializer(ModelSerializer):
    class Meta:
        model = CommentCourse
        fields = '__all__'


class CommentTeacherSerializer(ModelSerializer):
    class Meta:
        model = CommentTeacher
        fields = '__all__'


class CommentStudyPartnerSerializer(ModelSerializer):
    class Meta:
        model = CommentStudyPartner
        fields = '__all__'


# Serializers for Entity
class CommentCourseEntitySerializer(ModelSerializer):
    class Meta:
        model = CommentCourse
        exclude = ['id', 'entity']


class CommentTeacherEntitySerializer(ModelSerializer):
    class Meta:
        model = CommentTeacher
        exclude = ['id', 'entity']


class CommentStudyPartnerEntitySerializer(ModelSerializer):
    class Meta:
        model = CommentStudyPartner
        exclude = ['id', 'entity']

