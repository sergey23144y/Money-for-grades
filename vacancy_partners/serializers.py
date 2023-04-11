from rest_framework.serializers import ModelSerializer

from vacancy_partners.models import VacancyPartner


class VacancyPartnerViewSetSerializer(ModelSerializer):
    class Meta:
        model = VacancyPartner
        fields = '__all__'