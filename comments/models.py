from django.db import models


from users.models import User
from courses.models import Course
from teachers.models import Teacher
from study_partners.models import StudyPartner


# Create your models here.
class CommentCourse(models.Model):
    title = models.CharField(max_length=50, null=False)
    description = models.CharField(max_length=500, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    entity = models.ForeignKey(Course, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return self.title


class CommentTeacher(models.Model):
    title = models.CharField(max_length=50, null=False)
    description = models.CharField(max_length=500, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    entity = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return self.title


class CommentStudyPartner(models.Model):
    title = models.CharField(max_length=50, null=False)
    description = models.CharField(max_length=500, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    entity = models.ForeignKey(StudyPartner, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return self.title
