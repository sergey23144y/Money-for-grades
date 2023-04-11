from rest_framework.serializers import ModelSerializer

from study_partners.models import StudyPartner


class StudyPartnerViewSetSerializer(ModelSerializer):
    class Meta:
        model = StudyPartner
        fields = '__all__'