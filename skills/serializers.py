from rest_framework.relations import StringRelatedField
from rest_framework.serializers import ModelSerializer

from skills.models import Skill, SkillCategory


class SkillCategoryModelSerializer(ModelSerializer):
    class Meta:
        model = SkillCategory


class SkillModelSerializer(ModelSerializer):
    skill_category = SkillCategoryModelSerializer

    class Meta:
        model = Skill
        fields = '__all__'