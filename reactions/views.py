from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_405_METHOD_NOT_ALLOWED, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from reactions.models import ReactionsUsers, ReactionsEmployers
from users.models import User
from vacancy_partners.models import VacancyPartner


class ReactionsUsersAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User, email=request.data.get('email'))
        vacancy_partner = get_object_or_404(VacancyPartner, name=request.data.get('vacancy_partner'))
        reaction_type = request.data.get('reaction_type')

        if reaction_type not in ['like', 'dislike']:
            return Response(status=HTTP_400_BAD_REQUEST)

        if user.publication:
            ReactionsUsers.objects.create(user=user, vacancy_partner=vacancy_partner, reaction_type=reaction_type)
            return Response(status=HTTP_201_CREATED)

        else:
            return Response(status=HTTP_405_METHOD_NOT_ALLOWED)


class ReactionsEmployersAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        vacancy_partner = get_object_or_404(VacancyPartner, name=request.data.get('vacancy_partner'))
        user = get_object_or_404(User, email=request.data.get('email'))
        reaction_type = request.data.get('reaction_type')

        if reaction_type not in ['like', 'dislike']:
            return Response(status=HTTP_400_BAD_REQUEST)

        if user.publication:
            ReactionsEmployers.objects.create(vacancy_partner=vacancy_partner, user=user, reaction_type=reaction_type)
            return Response(status=HTTP_201_CREATED)

        else:
            return Response(status=HTTP_405_METHOD_NOT_ALLOWED)
