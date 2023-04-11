from django.http import QueryDict
from rest_framework.response import Response

from rest_framework.viewsets import ModelViewSet
from rest_framework import generics, status

from rest_framework.permissions import IsAdminUser, IsAuthenticated
from comments.permissions import IsOwnerCommentOrReadOnly

from comments.models import CommentCourse, CommentTeacher, CommentStudyPartner
from comments.serializers import CommentCourseSerializer, CommentTeacherSerializer, CommentStudyPartnerSerializer, \
    CommentCourseEntitySerializer, CommentTeacherEntitySerializer, CommentStudyPartnerEntitySerializer


# Create your views here.

# View for User
class CommentBaseUserViewSet(ModelViewSet):
    permission_classes = (IsOwnerCommentOrReadOnly,)

    def list(self, request, *args, **kwargs):
        queryset = self.queryset.filter(user=request.user.pk)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        data = QueryDict.copy(request.data)
        data['user'] = request.user.pk
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = QueryDict.copy(request.data)
        data['user'] = request.user.pk.hex
        serializer = self.get_serializer(instance, data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class CommentCourseUserViewSet(CommentBaseUserViewSet):
    serializer_class = CommentCourseSerializer
    queryset = CommentCourse.objects.all()


class CommentTeacherUserViewSet(CommentBaseUserViewSet):
    serializer_class = CommentTeacherSerializer
    queryset = CommentTeacher.objects.all()


class CommentStudyPartnerUserViewSet(CommentBaseUserViewSet):
    serializer_class = CommentStudyPartnerSerializer
    queryset = CommentStudyPartner.objects.all()


# Views for Admin
class CommentCourseAdminViewSet(ModelViewSet):
    permission_classes = (IsAdminUser,)
    queryset = CommentCourse.objects.all()
    serializer_class = CommentCourseSerializer


class CommentTeacherAdminViewSet(ModelViewSet):
    permission_classes = (IsAdminUser,)
    queryset = CommentTeacher.objects.all()
    serializer_class = CommentTeacherSerializer


class CommentStudyPartnerAdminViewSet(ModelViewSet):
    permission_classes = (IsAdminUser,)
    queryset = CommentStudyPartner.objects.all()
    serializer_class = CommentStudyPartnerSerializer


# Views for Entity
class CommentBaseEntityListApiView(generics.ListAPIView):
    queryset = None
    permission_classes = (IsOwnerCommentOrReadOnly,)

    def get(self, request, *args, **kwargs):
        queryset = self.queryset.filter(entity=kwargs.get('pk'))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CommentCourseEntityListApiView(CommentBaseEntityListApiView):
    queryset = CommentCourse.objects.all()
    serializer_class = CommentCourseEntitySerializer


class CommentTeacherEntityListApiView(CommentBaseEntityListApiView):
    queryset = CommentTeacher.objects.all()
    serializer_class = CommentTeacherEntitySerializer


class CommentStudyPartnerEntityListApiView(CommentBaseEntityListApiView):
    queryset = CommentStudyPartner.objects.all()
    serializer_class = CommentStudyPartnerEntitySerializer


