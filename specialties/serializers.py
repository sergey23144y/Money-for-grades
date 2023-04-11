from rest_framework.serializers import ModelSerializer

from specialties.models import Specialty, SpecialtyCategory


class SpecialtyViewSetSerializer(ModelSerializer):
    class Meta:
        model = Specialty
        fields = '__all__'


class SpecialtyCategoriesViewSetSerializer(ModelSerializer):
    class Meta:
        model = SpecialtyCategory
        fields = '__all__'