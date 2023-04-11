from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.utils import json

from promotions.models import Promotion
from rest_framework.viewsets import ModelViewSet

from promotions.serializers import PromotionModelViewSetSerializer


class PromotionModelViewSet(ModelViewSet):
    queryset = Promotion.objects.all()
    serializer_class = PromotionModelViewSetSerializer


class PromotionCityListAPIView(ListAPIView):
    queryset = Promotion.objects.all()
    serializer_class = PromotionModelViewSetSerializer

    def get_queryset(self, *args, **kwargs):
        promotions = Promotion.objects.filter(cities=self.kwargs['pk'])
        return promotions
