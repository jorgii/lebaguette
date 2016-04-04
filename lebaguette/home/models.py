from __future__ import unicode_literals

from django.db import models


class ServerMessage(models.Model):
    message = models.TextField('Message',
                               blank=False,
                               null=False)
    datetime_created = models.DateTimeField(auto_now_add=True)
