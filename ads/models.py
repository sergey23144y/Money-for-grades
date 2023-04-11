from django.db import models


class Advertisement(models.Model):
    name = models.CharField(max_length=64, blank=True)
    url = models.URLField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Реклама'
        verbose_name_plural = 'Рекламки'
