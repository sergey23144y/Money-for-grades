from django.db import models
from django.core.exceptions import ObjectDoesNotExist


class VendorCodeField(models.CharField):
    def __init__(self, for_fields=None, *args, **kwargs):
        self.for_fields = for_fields
        super(VendorCodeField, self).__init__(*args, **kwargs)

    def pre_save(self, instance, add):
        if getattr(instance, self.attname) is None:
            try:
                qs = self.model.objects.all()
                if self.for_fields:
                    query = {field: getattr(instance, field) for field in self.for_fields}
                    qs = qs.filter(**query)
                last_item = qs.latest(self.attname)
                if last_item.vendor is None:
                    last_item.vendor = 0

                value = int(last_item.vendor) + 1
                value = str(value)
                value = str.rjust(value, 7, '0')
            except ObjectDoesNotExist:
                value = ''
            setattr(instance, self.attname, value)
            return value
        else:
            return super(VendorCodeField, self).pre_save(instance, add)
