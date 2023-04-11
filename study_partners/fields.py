from random import randint

from django.db import models
from django.core.exceptions import ObjectDoesNotExist


class CodeField(models.IntegerField):
    def __init__(self, for_fields=None, *args, **kwargs):
        self.for_fields = for_fields
        super(CodeField, self).__init__(*args, **kwargs)

    def get_random_code(self):
        return randint(100000, 999999)

    def pre_save(self, instance, add):
        if getattr(instance, self.attname) is None:
            try:
                qs = self.model.objects.all()
                if self.for_fields:
                    query = {field: getattr(instance, field) for field in self.for_fields}
                    qs = qs.filter(**query)
                value = self.get_random_code()
                codes = [q.code for q in qs]
                while value in codes:
                    value = self.get_random_code()
            except ObjectDoesNotExist:
                value = ''
            setattr(instance, self.attname, value)
            return value
        else:
            return super(CodeField, self).pre_save(instance, add)
