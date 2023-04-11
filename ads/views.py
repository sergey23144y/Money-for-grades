from rest_framework.viewsets import ModelViewSet

from ads.models import Advertisement
from ads.serializers import AdvertisementViewSetSerializer


class AdvertisementViewSet(ModelViewSet):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementViewSetSerializer
