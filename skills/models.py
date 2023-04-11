from django.db import models


class SkillCategory(models.Model):
    name = models.CharField(primary_key=True, max_length=64, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория навыка"
        verbose_name_plural = "Категории навыков"


class Skill(models.Model):
    name = models.CharField(max_length=128, blank=True)
    skill_category = models.ForeignKey(SkillCategory, on_delete=models.CASCADE, null=True)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(null=True, unique=True)

    def __str__(self):
        return f"[{str(self.skill_category)[0]}] {self.name}"

    class Meta:
        verbose_name = "Навык"
        verbose_name_plural = "Навыки"
