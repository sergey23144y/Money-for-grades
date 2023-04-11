import datetime
import urllib.request
import uuid
from datetime import date

import environ
import requests
from PIL import Image
from authemail.models import PasswordResetCode, SignupCode
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.utils.timezone import now
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from django.utils.translation import gettext as _
from social_core.pipeline.user import create_user

from django_back_api.settings import SOCIAL_AUTH_VK_OAUTH2_KEY, SOCIAL_AUTH_VK_OAUTH2_SECRET, VK_OAUTH2_REDIRECT_URL, \
    VK_API_VERSION, MEDIA_ROOT
from django_back_api.utils import check_token_expired, update_token, generate_email
from users.models import User, UserSkill, UserRateHistory, UserType, SalesFunnel, SalesChannel, UserVKId, City, Country, \
    University, School, SecondaryEducation, Language
from users.serializers import UserSkillModelViewSetSerializer, \
    UserRateHistoryModelViewSetSerializer, UserTypeModelViewSetSerializer, SalesFunnelModelViewSetSerializer, \
    SalesChannelModelViewSetSerializer, UserSerializer, UserViewSetSerializer

env = environ.Env()
environ.Env.read_env()


#

class UserSkillsListAPIView(ListAPIView):
    serializer_class = UserSkillModelViewSetSerializer

    def get_queryset(self, *args, **kwargs):
        user_uid = uuid.UUID(self.kwargs['pk'])
        user_skills = UserSkill.objects.filter(user=user_uid)
        return user_skills


class UserRateHistoryListAPIView(ListAPIView):
    serializer_class = UserRateHistoryModelViewSetSerializer

    def get_queryset(self, *args, **kwargs):
        user_uid = uuid.UUID(self.kwargs['pk'])
        user_rate = UserRateHistory.objects.filter(user=user_uid)
        return user_rate


class PasswordResetVerify(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        code = request.GET.get('code', '')

        try:
            password_reset_code = PasswordResetCode.objects.get(code=code)

            # Delete password reset code if older than expiry period
            delta = date.today() - password_reset_code.created_at.date()
            if delta.days > PasswordResetCode.objects.get_expiry_period():
                password_reset_code.delete()
                raise PasswordResetCode.DoesNotExist()

            content = {'success': _('Email address verified.')}
            return HttpResponseRedirect(f'{env("PASSWORD_RESET_REDIRECT_URL")}{code}')
            # Response(content, status=status.HTTP_200_OK)
        except PasswordResetCode.DoesNotExist:
            content = {'detail': _('Unable to verify user.')}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)


class SignupVerify(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        code = request.GET.get('code', '')
        verified = SignupCode.objects.set_user_is_verified(code)

        if verified:
            try:
                signup_code = SignupCode.objects.get(code=code)
                signup_code.delete()
            except SignupCode.DoesNotExist:
                pass
            # content = {'success': _('Email address verified.')}
            # return Response(content, status=status.HTTP_200_OK)
            return HttpResponseRedirect(f'{env("SIGNUP_SUCCESS_REDIRECT_URL")}')
        else:
            # content = {'detail': _('Unable to verify user.')}
            # return Response(content, status=status.HTTP_400_BAD_REQUEST)
            return HttpResponseRedirect(f'{env("SIGNUP_ERROR_REDIRECT_URL")}')


class UserMe(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get(self, request, format=None):
        return Response(self.serializer_class(request.user).data)

    def patch(self, request, format=None):
        me = User.objects.get(email=request.user)
        data = request.data
        serializer = UserSerializer(instance=me, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            me = serializer.save()
        return Response(self.serializer_class(me).data)


class UserViewSet(ModelViewSet):
    permission_classes = (IsAdminUser,)
    serializer_class = UserViewSetSerializer
    queryset = User.objects.all()


class UserTypeViewSet(ModelViewSet):
    queryset = UserType.objects.all()
    serializer_class = UserTypeModelViewSetSerializer


class SalesFunnelViewSet(ModelViewSet):
    queryset = SalesFunnel.objects.all()
    serializer_class = SalesFunnelModelViewSetSerializer


class SalesChannelViewSet(ModelViewSet):
    queryset = SalesChannel.objects.all()
    serializer_class = SalesChannelModelViewSetSerializer


class UserAuthorize(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    authentication_classes = [SessionAuthentication]

    def get(self, request, format=None):
        token = Token.objects.get(user=request.user)
        return HttpResponseRedirect('https://sokratapp.ru', headers={'Authorization': f'Token {token}'})


class VKOAuth(APIView):
    permission_classes = (AllowAny,)

    def get_response_user(self, request) -> dict:
        code = request.data.get('code')
        ACCESS_TOKEN_URL = 'https://oauth.vk.com/access_token'
        client_id = SOCIAL_AUTH_VK_OAUTH2_KEY
        client_secret = SOCIAL_AUTH_VK_OAUTH2_SECRET
        redirect_uri = VK_OAUTH2_REDIRECT_URL
        vk_api_version = VK_API_VERSION
        token_request_url = f'{ACCESS_TOKEN_URL}?' \
                            f'client_id={client_id}&' \
                            f'client_secret={client_secret}&' \
                            f'redirect_uri={redirect_uri}&' \
                            f'code={code}'
        req = requests.request('get', url=token_request_url)
        response = dict(req.json())
        access_token = response.get('access_token')
        user_vk_id = response.get('user_id')

        email = response.get('email')
        user_request_url = f'https://api.vk.com/method/users.get?' \
                           f'fields=bdate,photo_max_orig,email,city,country,nickname,schools,universities&' \
                           f'access_token={access_token}&' \
                           f'v={vk_api_version}'
        user_request = requests.request('get', url=user_request_url)
        response_user = dict(user_request.json())
        response_user['user_vk_id'] = user_vk_id
        response_user['email'] = email
        return response_user

    def get_user_data(self, func_response_user) -> dict:
        charfields = {}
        response_user = func_response_user.get('response')[0]
        charfields['email'] = response_user.get['email']
        charfields['user_vk_id'] = response_user.get['user_vk_id']

        first_name = response_user.get('first_name')
        charfields['first_name'] = first_name

        last_name = response_user.get('last_name')
        charfields['last_name'] = last_name

        middle_name = response_user.get('nickname')
        charfields['middle_name'] = middle_name

        bdate = response_user.get('bdate')
        bdate = datetime.datetime.strptime(bdate, '%d.%m.%Y')
        bdate = bdate.strftime("%Y-%m-%d")
        charfields['birthday'] = bdate

        photo_url = response_user.get('photo_max_orig')
        photo_path = MEDIA_ROOT / f'{func_response_user.get("user_vk_id")}.jpg'
        photo_path, _ = urllib.request.urlretrieve(photo_url, photo_path)
        charfields['avatar'] = photo_path
        user = {'charfields': charfields}

        vk_city = response_user.get('city')
        if vk_city:
            vk_city_title = vk_city.get('title')
            city, created = City.objects.get_or_create(vk_city_title)
        else:
            city = 0
        foreigns = {'city': city}

        vk_country = response_user.get('country')
        if vk_country:
            vk_country_title = vk_country.get('title')
            country, created = Country.objects.get_or_create(name=vk_country_title)
        else:
            country = 0
        foreigns['country'] = country

        schools = []
        secondary_educations = []
        universities = []
        vk_schools = response_user.get('schools')
        for s in vk_schools:
            school_title = s.get('name')
            school_type = s.get('type')
            if school_type and school_type in range(0, 5):
                school, created = School.objects.get_or_create(name=school_title)
                schools.append(school)
            elif school_type and school_type:
                secondary_education, created = SecondaryEducation.objects.get_or_create(name=school_title)
                secondary_educations.append(secondary_education)
        foreigns['school'] = schools
        foreigns['secondary_education'] = secondary_educations

        vk_universities = response_user.get('universities')
        for u in vk_universities:
            vk_university_title = u.get('name')
            university, created = University.objects.get_or_create(name=vk_university_title)
            universities.append(university)
        foreigns['university'] = universities
        user['foreigns'] = foreigns
        return user

    def save_user(self, user_data: dict):
        user = User.objects.create(email=user_data.get('email'), is_staff=False, is_active=True, is_superuser=False,
                                   last_login=now, is_verified=False
                                   )
        charfields = user_data.get('charfields')
        for attribute in charfields.keys():
            if user_data.get(attribute):
                setattr(user, attribute, user_data.get(attribute))

        foreigns = user_data.get('foreigns')
        for attribute in foreigns.keys():
            user.attribute.set(foreigns.get(attribute))
            
        default = None
        # if user_data.get('is_verified'):
        #     user.is_verified = True
        # birthday =
        #
        # last_name =
        #
        # middle_name =
        #
        # avatar = f'{user_vk_id}.jpg'
        # first_name = user_data.get('first_name')
        # if first_name:
        #     user.first_name = first_name
        # secondary_educations = user_data.get('secondary')
        # if secondary_educations:
        #     user.secondary_education.set(secondary_educations)
        # if universities:
        #     user.universities.set(universities)
        # if schools:
        #     user.school.set(schools)
        # if city:
        #     user.city.set(city)
        # if country:
        #     user.country.set(country)
        user.set_password(raw_password=None)
        user.save()
        register_group = Group.objects.filter(name='registered')
        user.groups.set(register_group)

    def post(self, request):
        response_user = self.get_response_user(request)
        user_data = self.get_user_data(response_user)
        email = user_data.get('email')
        if email:
            username = email
            user = User.objects.filter(email=email).first()
            vk_id_user = UserVKId.objects.filter(vk_id=user_data.get('user_vk_id')).first()
            if not user and not vk_id_user:
                now = timezone.now()
                email = User.objects.normalize_email(email)
                user_data['email'] = email
                user_data['date_joined'] = now

                vk_user = UserVKId.objects.create(user=user, vk_id=user_vk_id)
                vk_user.save()
            elif not user and vk_id_user:
                now = timezone.now()
                email = User.objects.normalize_email(email)
                user = User.objects.get(uid=vk_id_user.user.uid) \
                    .update(email=email, is_staff=False, is_active=True, is_superuser=False, is_verified=True,
                            last_login=now, first_name=first_name, birthday=bdate, last_name=last_name,
                            middle_name=middle_name
                            )
                user.avatar = photo_path
                if secondary_educations:
                    user.secondary_education.set(secondary_educations)
                if universities:
                    user.universities.set(universities)
                if schools:
                    user.school.set(schools)
                if city:
                    user.city.set(city)
                if country:
                    user.country.set(country)
                user.save()
        else:
            email = generate_email()
            username = first_name if first_name else user_vk_id
            try:
                vk_id_user = UserVKId.objects.get(vk_id=user_vk_id)
            except ObjectDoesNotExist:
                vk_id_user = 0
            if vk_id_user:
                user = User.objects.get(uid=vk_id_user.user_id)
            else:
                now = timezone.now()
                register_group = Group.objects.filter(name='registered')
                user = User.objects.create(is_staff=False, is_active=True, is_superuser=False,
                                           is_verified=False, last_login=now, date_joined=now, first_name=first_name,
                                           birthday=bdate, last_name=last_name, middle_name=middle_name, email=email
                                           )
                user.avatar = photo_path
                if secondary_educations:
                    user.secondary_education.set(secondary_educations)
                if universities:
                    user.universities.set(universities)
                if schools:
                    user.school.set(schools)
                if city:
                    user.city.set(city)
                if country:
                    user.country.set(country)
                user.set_password(raw_password=None)
                user.save()
                user.groups.set(register_group)
                vk_user = UserVKId.objects.create(user=user, vk_id=user_vk_id)
                vk_user.save()
        token = update_token(user)
        return Response({'token': f'{token}', 'username': username})


def get_languages_from_hh():
    languages_url = 'https://api.hh.ru/languages'
    languages_request = requests.request('get', url=languages_url)
    response_languages = languages_request.json()
    for language in response_languages:
        language_name = language['name']
        if not Language.objects.filter(name=language_name).exists():
            add_language = Language.objects.create(name=language_name)
