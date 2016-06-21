from datetime import datetime, date
import os
import requests

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from lebaguette.settings import MEDIA_URL


class MediaItem(models.Model):
    # General properties
    MEDIA_TYPE_CHOICES = (
        ('series', 'TV Show'),
        ('movie', 'Movie'),
        ('episode', 'Episode'),
    )
    media_type = models.CharField(max_length=7, choices=MEDIA_TYPE_CHOICES)
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
    season = models.IntegerField(null=True, blank=True)
    episode = models.IntegerField(null=True, blank=True)
    tv_show = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True)

    def save_and_create_request(self, requested_by, status, *args, **kwargs):
        super(MediaItem, self).save(*args, **kwargs)
        user = User.objects.get(username='cronjob')
        media_request = Request.objects.create(
            status=status,
            media_item=self,
            requested_by=requested_by)
        if requested_by == user:
            media_request.approve(requested_by)
        media_request.save()

    def get_poster_url(self):
        try:
            if self.media_type == 'episode':
                return self.tv_show.poster.url
            else:
                return self.poster.url
        except ValueError:
            return None

    def get_latest_episode(self):
        try:
            latest_episode = MediaItem.objects.filter(
                tv_show=self).order_by('-released')[0]
        except IndexError:
            latest_episode = None
        return latest_episode

    @classmethod
    def create_media_from_imdbid(cls, imdb_id):
        media_item = cls(imdb_id=imdb_id)
        media_request = media_item.get_data_from_api()
        if media_request['Type'] == 'episode':
            return None
        media_item.media_type = media_request['Type']
        media_item.title = media_request['Title']
        media_item.released = datetime.strptime(
                media_request['Released'], '%d %b %Y').date()
        return media_item

    def create_new_episodes(self, episode, season, requested_by, status):
        season_request = self.get_data_from_api(season)
        total_seasons = range(season, int(season_request['totalSeasons']))
        while season_request['Response'] == 'True':
            for api_episode in season_request['Episodes'][episode:]:
                try:
                    if not MediaItem.objects.filter(
                                episode=int(api_episode['Episode']),
                                season=season,
                                imdb_id=api_episode['imdbID']).exists() and \
                            date.today() >= datetime.strptime(
                                api_episode['Released'],
                                '%Y-%m-%d').date():
                        new_episode = MediaItem.objects.create(
                            media_type='episode',
                            title=api_episode['Title'],
                            released=datetime.strptime(
                                api_episode['Released'],
                                '%Y-%m-%d').date(),
                            imdb_id=api_episode['imdbID'],
                            season=season,
                            episode=int(api_episode['Episode']),
                            tv_show=self)
                        new_episode.save_and_create_request(
                            requested_by,
                            status)
                except ValueError:
                    continue
            season += 1
            season_request = self.get_data_from_api(season)

    def get_data_from_api(self, season=None):
        try:
            media_request = requests.get(
                'http://www.omdbapi.com/?i=' +
                self.imdb_id +
                ('&Season=' + str(season) if season else '') +
                '&plot=short&r=json')
        except requests.exceptions.ConnectionError:
            print('There was an error connecting to the api. ')
        except requests.exceptions.HTTPError:
            print('Invalid HTTP response received. ')
        except requests.exceptions.Timeout:
            print('The connection to the api timed out. ')
        except requests.exceptions.TooManyRedirects:
            print('There have been too many redirects. ')
        return media_request.json()

    def __str__(self):
        if self.media_type == 'series':
            return (self.title + ' (TV Show)')
        elif self.media_type == 'episode':
            return (
                self.tv_show.title +
                (' S0' if self.season < 10 else ' S') + str(self.season) +
                ('E0' if self.episode < 10 else 'E') + str(self.episode))
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
