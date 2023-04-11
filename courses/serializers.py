import random
from collections import OrderedDict

from rest_framework import serializers
from rest_framework.fields import SkipField
from rest_framework.relations import StringRelatedField, PKOnlyObject
from rest_framework.serializers import ModelSerializer

from courses.models import CourseCategory, Course, CoursePrice, CourseSkillLevelWeight, CourseSubcategory, PayType, \
    TypeOfLearning, Payment, Book, Software, StudyProgram, PersonalityType, TypeOfTraining, CourseOrigin, Status, \
    CourseCommit

class CourseCategoryViewSetSerializer(ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = '__all__'


class CourseViewSetSerializer(ModelSerializer):

    pay_type = StringRelatedField()
    study_partner = StringRelatedField()
    type_of_learning = StringRelatedField()
    study_program = StringRelatedField()
    payment = StringRelatedField()
    teachers = StringRelatedField(many=True)

    class Meta:
        model = Course
        fields = '__all__'


class CourseApiViewSerializer(ModelSerializer):
    pay_type = StringRelatedField()
    study_partner = StringRelatedField()
    type_of_learning = StringRelatedField()
    study_program = StringRelatedField()
    payment = StringRelatedField()
    teachers = StringRelatedField(many=True)

    class Meta:
        model = Course
        exclude = ['vendor', 'course_origin', 'status']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['online'] = random.randint(0, 1000)
        return ret


class CoursePriceViewSetSerializer(ModelSerializer):
    course = StringRelatedField()

    class Meta:
        model = CoursePrice
        fields = '__all__'


class CourseSkillLevelWeightViewSetSerializer(ModelSerializer):
    skill = StringRelatedField()

    class Meta:
        model = CourseSkillLevelWeight
        fields = '__all__'


class CourseBaseCategoryViewSetSerializer(ModelSerializer):
    course = StringRelatedField()

    class Meta:
        model = CourseSubcategory
        fields = '__all__'


class PayTypeViewSetSerializer(ModelSerializer):
    course = StringRelatedField()

    class Meta:
        model = PayType
        fields = '__all__'


class TypeOfLearningViewSetSerializer(ModelSerializer):
    course = StringRelatedField()

    class Meta:
        model = TypeOfLearning
        fields = '__all__'


class PaymentViewSetSerializer(ModelSerializer):
    course = StringRelatedField()

    class Meta:
        model = Payment
        fields = '__all__'


class BookViewSetSerializer(ModelSerializer):
    course = StringRelatedField()

    class Meta:
        model = Book
        fields = '__all__'


class SoftwareViewSetSerializer(ModelSerializer):
    course = StringRelatedField()

    class Meta:
        model = Software
        fields = '__all__'


class StudyProgramViewSetSerializer(ModelSerializer):
    course = StringRelatedField()

    class Meta:
        model = StudyProgram
        fields = '__all__'


class PersonalityTypeViewSetSerializer(ModelSerializer):
    course = StringRelatedField()

    class Meta:
        model = PersonalityType
        fields = '__all__'


class TypeOfTrainingViewSetSerializer(ModelSerializer):
    course = StringRelatedField()

    class Meta:
        model = TypeOfTraining
        fields = '__all__'


class CourseOriginViewSetSerializer(ModelSerializer):
    course = StringRelatedField()

    class Meta:
        model = CourseOrigin
        fields = '__all__'


class StatusViewSetSerializer(ModelSerializer):
    course = StringRelatedField()

    class Meta:
        model = Status
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        exclude = ['vendor', 'course_origin', 'status']


class CourseCommitSerializer(ModelSerializer):
    courses = CourseSerializer(many=True, read_only=True)
    class Meta:
        model = CourseCommit
        fields = "__all__"