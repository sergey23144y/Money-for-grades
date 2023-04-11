from django.db import models
# from courses.models import Course


# Create your models here.
class WebmasterCategory(models.Model):
    id = models.CharField(primary_key=True, max_length=6)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


# class WebmasterFeed(models.Model):
#     uuid = models.UUIDField(editable=False)
#     course = models.ForeignKey(Course, on_delete=models.CASCADE, editable=False)
