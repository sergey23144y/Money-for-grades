from django.contrib import admin

from courses.models import Course, CourseCategory, CourseSubcategory, CoursePrice, CourseCommit, Payment, PayType


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    search_fields = ("name__startswith",)
admin.site.register(CourseCategory)
admin.site.register(CourseSubcategory)
admin.site.register(CoursePrice)
admin.site.register(CourseCommit)
admin.site.register(PayType)