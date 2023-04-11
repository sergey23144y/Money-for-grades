from rest_framework.serializers import ModelSerializer

from ads.models import Advertisement


class AdvertisementViewSetSerializer(ModelSerializer):
    class Meta:
        model = Advertisement
        fields = '__all__'
