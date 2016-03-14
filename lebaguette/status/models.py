from __future__ import unicode_literals

from django.db import models


class Services(models.Model):
    service_name = models.CharField('Service Name', max_length=255, blank=False, null=False)
    datetime_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.service_name
