import uuid

from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet

from vacancies.models import VacancyCategory, Vacancy, VacancyRequirement, TypeOfWork, WorkSchedule
from vacancies.serializers import VacancyCategoryViewSetSerializer, VacancyViewSetSerializer, \
    VacancyRequirementModelViewSetSerializer, TypeOfWorkModelViewSetSerializer, WorkScheduleModelViewSetSerializer


class VacancyCategoryViewSet(ModelViewSet):
    queryset = VacancyCategory.objects.all()
    serializer_class = VacancyCategoryViewSetSerializer


class VacancyViewSet(ModelViewSet):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyViewSetSerializer


class VacancyRequirementListAPIView(ListAPIView):
    # queryset = VacancyRequirement.objects.all()
    serializer_class = VacancyRequirementModelViewSetSerializer

    def get_queryset(self, *args, **kwargs):
        vacancy = uuid.UUID(self.kwargs['pk'])
        vac_reqs = VacancyRequirement.objects.filter(vacancy=vacancy)
        return vac_reqs


class TypeOfWorkViewSet(ModelViewSet):
    queryset = TypeOfWork.objects.all()
    serializer_class = TypeOfWorkModelViewSetSerializer


class WorkScheduleViewSet(ModelViewSet):
    queryset = WorkSchedule.objects.all()
    serializer_class = WorkScheduleModelViewSetSerializer
