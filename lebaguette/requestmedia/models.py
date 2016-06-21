from datetime import datetime, date
import os
import requests

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from lebaguette.settings import MEDIA_URL


class MediaItem(models.Model):
    # General properties
    MEDIA_TYPE_CHOICES = (
        ('series', 'TV Show'),
        ('movie', 'Movie'),
        ('episode', 'Episode'),
    )
    media_type = models.CharField(max_length=2, choices=MEDIA_TYPE_CHOICES)
    title = models.CharField('Title',
                             max_length=255,
                             blank=False,
                             null=False)
    released = models.DateField()
    imdb_id = models.CharField('IMDB ID',
                               max_length=255,
                               blank=False,
                               null=False)
    poster = models.ImageField(
        upload_to='posters/',
        blank=True,
        null=True)
    # TV Show properties
    media_completed = models.BooleanField(default=False)
    # Episode properties
    season = models.IntegerField()
    episode = models.IntegerField()
    tv_show = models.ForeignKey('self', on_delete=models.CASCADE)

    def get_poster_url(self):
        try:
            return self.poster.url
        except ValueError:
            return None

    def get_latest_episode(self):
        return MediaItem.objects.filter(tv_show=self).order_by('-released')[0]

    def __str__(self):
        if self.media_type == 'TV':
            return (self.title + '(TV Show)')
        elif slef.media_type == 'EP':
            return (
                self.tv_show.title +
                (' S0' if self.season < 10 else ' S') + self.season +
                (' E0' if self.episode < 10 else ' E') + self.episode)
        else:
            return (self.title)


class Request(models.Model):
    STATUS_CHOICES = (
        ('N', 'New'),
        ('A', 'Approved'),
        ('R', 'Rejected'),
        ('C', 'Completed')
    )
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    media_item = models.OneToOneField(MediaItem, null=True, blank=True)
    requested_by = models.ForeignKey('auth.User', related_name="+")
    datetime_requested = models.DateTimeField(auto_now_add=True)
    completed_by = models.ForeignKey(
        'auth.User',
        related_name="+",
        null=True, blank=True)
    datetime_completed = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(
        'auth.User',
        related_name="+",
        null=True,
        blank=True)
    datetime_approved = models.DateTimeField(null=True, blank=True)
    rejected_by = models.ForeignKey(
        'auth.User',
        related_name="+",
        null=True,
        blank=True)
    datetime_rejected = models.DateTimeField(null=True, blank=True)

    class Meta:
        permissions = {
            ('view', 'Can view requests'),
            ('approve', 'Can approve requests'),
            ('reject', 'Can reject requests'),
            ('complete', 'Can complete requests')
        }

    def complete(self, completed_by):
        self.status = 'C'
        self.completed_by = completed_by
        self.datetime_completed = timezone.now()
        self.save()

    def approve(self, approved_by):
        self.status = 'A'
        self.approved_by = approved_by
        self.datetime_approved = timezone.now()
        self.save()

    def reject(self, rejected_by):
        self.status = 'R'
        self.rejected_by = rejected_by
        self.datetime_rejected = timezone.now()
        self.save()

    def __str__(self):
        text = str(self.media_item) +\
            ' by ' +\
            str(self.requested_by.first_name) +\
            ' ' +\
            str(self.requested_by.last_name)
        return text
