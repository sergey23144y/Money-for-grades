from django.contrib.auth import get_user_model
from rest_framework.relations import StringRelatedField
from rest_framework.serializers import ModelSerializer

from users.models import User, UserSkill, UserRateHistory, UserType, SalesFunnel, SalesChannel


class UserSkillModelViewSetSerializer(ModelSerializer):
    skill = StringRelatedField()

    class Meta:
        model = UserSkill


class UserRateHistoryModelViewSetSerializer(ModelSerializer):
    class Meta:
        model = UserRateHistory


class UserTypeModelViewSetSerializer(ModelSerializer):
    class Meta:
        model = UserType


class SalesFunnelModelViewSetSerializer(ModelSerializer):
    class Meta:
        model = SalesFunnel


class SalesChannelModelViewSetSerializer(ModelSerializer):
    class Meta:
        model = SalesChannel


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'middle_name', 'birthday', 'secondary_education',
                  'rating', 'current_rate', 'rate', 'money_for_grades', 'skills', 'specialty_category', 'specialties',
                  'telegram', 'phone', 'vacancy', 'university', 'school', 'avatar', 'study_partners',
                  'personality_type', 'country', 'city', 'bonus_account', 'publication', 'about_yourself',
                  'languages', 'experience', 'level_of_professionalism', 'vocational_education', 'higher_education',
                  'second_higher_education', 'additional_education'
                  )


class UserViewSetSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
