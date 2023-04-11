from django.contrib.admin import ModelAdmin

from ads.models import Advertisement
from courses.models import Course, CoursePrice, CourseCategory, CourseSubcategory, CourseCommit
from promotions.models import Promotion
from skills.models import SkillCategory, Skill
from specialties.models import Specialty, SpecialtyCategory
from study_partners.models import StudyPartner
from teachers.models import Teacher
from users.models import User
from vacancies.models import Vacancy
from orders.models import Order
from vacancy_partners.models import VacancyPartner
from django.contrib import admin
from django.contrib.auth import get_user_model
from authemail.admin import EmailUserAdmin


admin.site.unregister(get_user_model())
@admin.register(get_user_model())
class UserAdmin(EmailUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'middle_name', 'birthday', 'telegram', 'phone',
                                      'rating', 'current_rate', 'rate', 'money_for_grades', 'specialty_category',
                                      'specialties', 'skills', 'vocational_education', 'higher_education',
                                      'second_higher_education', 'additional_education', 'experience',
                                      'level_of_professionalism', 'personality_type', 'languages', 'about_yourself',
                                      'publication')}),
        ('Permissions', {'fields': (
            'is_active', 'is_staff', 'is_superuser', 'is_verified', 'groups', 'user_permissions'
        )}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Custom info', {'fields': ('uid', 'avatar')}),
    )
    readonly_fields = ('rating',)

# Hiding service models from users without 'users.can_moderate_tasks' permission
# Authemail
from authemail.admin import SignupCode, SignupCodeAdmin, PasswordResetCode, PasswordResetCodeAdmin,\
EmailChangeCode, EmailChangeCodeAdmin
admin.site.unregister(SignupCode)
admin.site.unregister(PasswordResetCode)
admin.site.unregister(EmailChangeCode)

class Hider:
    def has_module_permission(self, request):
        return request.user.has_perm('users.can_moderate_tasks')

class PasswordResetCodeAdminHidden(Hider, PasswordResetCodeAdmin):
    ...

class SignupCodeAdminHidden(Hider, SignupCodeAdmin):
    ...

class EmailChangeCodeAdminHidden(Hider, EmailChangeCodeAdmin):
    ...

admin.site.register(PasswordResetCode, PasswordResetCodeAdminHidden)
admin.site.register(SignupCode, SignupCodeAdminHidden)
admin.site.register(EmailChangeCode, EmailChangeCodeAdminHidden)

# Celery and periodic tasks
from django_celery_beat.admin import ClockedScheduleAdmin, ClockedSchedule, CrontabSchedule, IntervalSchedule, SolarSchedule, PeriodicTaskAdmin, PeriodicTask

admin.site.unregister(IntervalSchedule)
admin.site.unregister(CrontabSchedule)
admin.site.unregister(SolarSchedule)
admin.site.unregister(ClockedSchedule)
admin.site.unregister(PeriodicTask)


class IntervalScheduleAdminHider(Hider, admin.ModelAdmin):
    ...

class CrontabScheduleAdminHider(Hider, admin.ModelAdmin):
    ...

class SolarScheduleAdminHider(Hider, admin.ModelAdmin):
    ...

class ClockedScheduleAdminHider(Hider, ClockedScheduleAdmin):
    ...

class PeriodicTaskAdminHider(Hider, PeriodicTaskAdmin):
    ...


admin.site.register(IntervalSchedule, IntervalScheduleAdminHider)
admin.site.register(CrontabSchedule, CrontabScheduleAdminHider)
admin.site.register(SolarSchedule, SolarScheduleAdminHider)
admin.site.register(ClockedSchedule, ClockedScheduleAdminHider)
admin.site.register(PeriodicTask, PeriodicTaskAdminHider)

# BTW lets protect tokens

from rest_framework.authtoken.admin import TokenProxy, TokenAdmin

admin.site.unregister(TokenProxy)

class TokenAdminHider(Hider, TokenAdmin):
    ...

admin.site.register(TokenProxy, TokenAdminHider)