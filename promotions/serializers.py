from rest_framework.relations import StringRelatedField
from rest_framework.serializers import ModelSerializer

from promotions.models import Promotion


class PromotionModelViewSetSerializer(ModelSerializer):
    #vacancy_partner = StringRelatedField()
    #study_partner = StringRelatedField()

    class Meta:
        model = Promotion
        exclude = ('cities',)


