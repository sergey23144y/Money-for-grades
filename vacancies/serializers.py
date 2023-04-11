from rest_framework.relations import StringRelatedField
from rest_framework.serializers import ModelSerializer

from vacancies.models import VacancyCategory, Vacancy, VacancyRequirement, TypeOfWork, WorkSchedule


class VacancyCategoryViewSetSerializer(ModelSerializer):
    class Meta:
        model = VacancyCategory
        fields = '__all__'


class VacancyViewSetSerializer(ModelSerializer):
    vacancy_partner = StringRelatedField()
    work_schedule = StringRelatedField()
    personality_type = StringRelatedField()
    courses = StringRelatedField(many=True)

    class Meta:
        model = Vacancy
        fields = '__all__'


class VacancyRequirementModelViewSetSerializer(ModelSerializer):
    skill = StringRelatedField()

    class Meta:
        model = VacancyRequirement
        fields = '__all__'


class TypeOfWorkModelViewSetSerializer(ModelSerializer):

    class Meta:
        model = TypeOfWork
        fields = '__all__'


class WorkScheduleModelViewSetSerializer(ModelSerializer):

    class Meta:
        model = WorkSchedule
        fields = '__all__'
