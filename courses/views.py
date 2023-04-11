import random
import uuid

from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from courses.models import CourseCategory, Course, CoursePrice, CourseSkillLevelWeight, CourseSubcategory, PayType, \
    TypeOfLearning, Payment, Book, Software, StudyProgram, PersonalityType, TypeOfTraining, CourseOrigin, Status, \
    CourseCommit
from courses.serializers import CourseCategoryViewSetSerializer, CourseViewSetSerializer, CoursePriceViewSetSerializer, \
    CourseSkillLevelWeightViewSetSerializer, CourseBaseCategoryViewSetSerializer, PayTypeViewSetSerializer, \
    TypeOfLearningViewSetSerializer, PaymentViewSetSerializer, BookViewSetSerializer, SoftwareViewSetSerializer, \
    StudyProgramViewSetSerializer, PersonalityTypeViewSetSerializer, TypeOfTrainingViewSetSerializer, \
    CourseOriginViewSetSerializer, StatusViewSetSerializer, CourseApiViewSerializer, CourseCommitSerializer

from rest_framework import mixins, generics


class CourseCategoryListAPIView(ListAPIView):
    serializer_class = CourseCategoryViewSetSerializer

    def get_queryset(self, *args, **kwargs):
        query = self.kwargs.get('pk')
        if query == 'all':
            course = CourseCategory.objects.all()
        else:
            course = CourseCategory.objects.filter(slag=query)
        return course


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseViewSetSerializer
    permission_classes = (IsAdminUser,)


class CourseListAPIView(ListAPIView):
    serializer_class = CourseApiViewSerializer

    def get_queryset(self, *args, **kwargs):
        query = self.kwargs.get('pk')
        if query == 'all':
            course = Course.objects.all()
        else:
            course = Course.objects.filter(slag=query)
        return course


class CoursePriceViewSet(ModelViewSet):
    queryset = CoursePrice.objects.all()
    serializer_class = CoursePriceViewSetSerializer


class CourseSkillLevelWeightListAPIView(ListAPIView):
    # queryset = CourseSkillLevelWeight.objects.all()
    serializer_class = CourseSkillLevelWeightViewSetSerializer

    def get_queryset(self, *args, **kwargs):
        course_uid = uuid.UUID(self.kwargs['pk'])
        course_skill = CourseSkillLevelWeight.objects.filter(course=course_uid)
        return course_skill


class CourseBaseCategoryLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 100


class CourseBaseCategoryListAPIView(ListAPIView):
    serializer_class = CourseBaseCategoryViewSetSerializer
    pagination_class = CourseBaseCategoryLimitOffsetPagination

    def get_queryset(self, *args, **kwargs):
        query = self.kwargs.get('pk')
        if query == 'all':
            course = CourseSubcategory.objects.all()
        else:
            course = CourseSubcategory.objects.filter(slag=query)
        return course


class CourseByBaseCourseCategoryListAPIView(ListAPIView):
    serializer_class = CourseApiViewSerializer

    def get_queryset(self, *args, **kwargs):
        query = self.kwargs.get('pk')
        course_category = get_object_or_404(CourseSubcategory, slag=query)
        course = Course.objects.filter(course_base_category=course_category.id)
        return course


class PayTypeViewSet(ModelViewSet):
    queryset = PayType.objects.all()
    serializer_class = PayTypeViewSetSerializer


class TypeOfLearningViewSet(ModelViewSet):
    queryset = TypeOfLearning.objects.all()
    serializer_class = TypeOfLearningViewSetSerializer


class PaymentViewSet(ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentViewSetSerializer


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookViewSetSerializer


class SoftwareViewSet(ModelViewSet):
    queryset = Software.objects.all()
    serializer_class = SoftwareViewSetSerializer


class StudyProgramViewSet(ModelViewSet):
    queryset = StudyProgram.objects.all()
    serializer_class = StudyProgramViewSetSerializer


class PersonalityTypeViewSet(ModelViewSet):
    queryset = PersonalityType.objects.all()
    serializer_class = PersonalityTypeViewSetSerializer


class TypeOfTrainingViewSet(ModelViewSet):
    queryset = TypeOfTraining.objects.all()
    serializer_class = TypeOfTrainingViewSetSerializer


class CourseOriginViewSet(ModelViewSet):
    queryset = CourseOrigin.objects.all()
    serializer_class = CourseOriginViewSetSerializer


class StatusViewSet(ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusViewSetSerializer


class CourseCommitViewSet(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = CourseCommit.objects.all()
    serializer_class = CourseCommitSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class CourseCommitRetrieve(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = CourseCommit.objects.all()
    serializer_class = CourseCommitSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class CourseCommitUpdate(mixins.UpdateModelMixin, generics.GenericAPIView):
    queryset = CourseCommit.objects.all()
    serializer_class = CourseCommitSerializer
    permission_classes = (IsAdminUser,)

    def update(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class CourseCommitCreate(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = CourseCommit.objects.all()
    serializer_class = CourseCommitSerializer
    permission_classes = (IsAdminUser,)

    def put(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)