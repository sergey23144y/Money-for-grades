from django.contrib import admin
from reactions.models import ReactionsEmployers, ReactionsUsers


@admin.register(ReactionsEmployers)
class ReactionsEmployersAdmin(admin.ModelAdmin):
    readonly_fields = ('vacancy_partner', 'user', 'reaction_type',)


@admin.register(ReactionsUsers)
class ReactionsUsersAdmin(admin.ModelAdmin):
    readonly_fields = ('user', 'vacancy_partner', 'reaction_type',)
