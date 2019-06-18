from datetime import datetime, date
from urllib.parse import urlparse
import os
import requests
import logging

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.files import File
from django.conf import settings

logger = logging.getLogger('django.info')


def get_media_json(media_type, media_request):
    if media_type == 'movie':
        if len(media_request.get('movie_results')) != 1:
            logger.error(
                'The response returned too many results of '
                'type {}!'.format(media_type))
            raise Exception(
                'Too many results!',
                'The response returned too many results of '
                'type {}!'.format(media_type)
            )
        return media_request['movie_results'][0]
    elif media_type == 'series':
        if len(media_request.get('tv_results')) != 1:
            logger.error(
                'The response returned too many results of '
                'type {}!'.format(media_type))
            raise Exception(
                'Too many results!',
                'The response returned too many results of '
                'type {}!'.format(media_type)
            )
        return media_request['tv_results'][0]


def get_media_type(media_request):
    if media_request.get('movie_results') != []:
        return 'movie'
    elif media_request.get('tv_results') != []:
        return 'series'
    logger.error('No compatible media type discovered in the response!')
    raise Exception(
        'No compatible media',
        'No compatible media type discovered in the response!'
    )


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
    released = models.DateField(blank=True, null=True)
    imdb_id = models.CharField('IMDB ID',
                               max_length=255,
                               blank=False,
                               null=False,
                               unique=True)
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

    def save(self, *args, **kwargs):
        if not (self.poster or self.media_type == 'episode'):
            media_request = self.get_data_from_api()
            media_request = get_media_json(self.media_type, media_request)
            if 'poster_path' in media_request:
                image_url = 'https://image.tmdb.org/t/p/w92{}'.format(
                    media_request.get('poster_path')
                )
                try:
                    request = requests.get(image_url)
                    file_name = os.path.basename(urlparse(image_url).path)
                    try:
                        f = open('/tmp/tmp_logo.png', 'wb')
                        f.write(request.content)
                        f = open('/tmp/tmp_logo.png', 'rb')
                        django_file = File(f)
                        self.poster.save(file_name, django_file, save=True)
                    except IOError as e:
                        logger.error(e)
                    finally:
                        f.close()
                        os.remove('/tmp/tmp_logo.png')
                except requests.exceptions.MissingSchema:
                    super(MediaItem, self).save(*args, **kwargs)
        super(MediaItem, self).save(*args, **kwargs)

    def save_and_create_request(self, requested_by, status):
        self.save()
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
        logger.info(
            'Attempting to add media item with imdb_id {}'.format(imdb_id))
        media_item = cls(imdb_id=imdb_id)
        media_request = media_item.get_data_from_api()
        media_item.media_type = get_media_type(media_request)
        media_request = get_media_json(media_item.media_type, media_request)
        if media_item.media_type == 'series':
            media_item.title = media_request.get('name', 'Not Found')
            if 'first_air_date' in media_request:
                media_item.released = datetime.strptime(
                    media_request['first_air_date'], '%Y-%m-%d'
                ).date()
        else:
            media_item.title = media_request.get('title', 'Not Found')
            if 'release_date' in media_request:
                media_item.released = datetime.strptime(
                    media_request['release_date'], '%Y-%m-%d'
                ).date()
        return media_item

    def create_new_episodes(self, episode, season, requested_by, status):
        total_seasons = season
        while season <= total_seasons:
            season_request = self.get_data_from_api(season)
            total_seasons = int(season_request['totalSeasons'])
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
                        logger.info("Successfully added {0}!".format(
                            str(new_episode)))
                    else:
                        break
                except ValueError as e:
                    logger.info(
                        "Error adding S{0}E{1}: {2}! Skipping..".format(
                            season,
                            int(api_episode['Episode']),
                            e))
                    continue
            season += 1
            episode = 0

    def get_data_from_api(self, season=None):
        url = (
            f'https://api.themoviedb.org/3/find/{self.imdb_id}?'
            f'api_key={settings.TMDB_APIKEY}&'
            'language=en-US&external_source=imdb_id')
        try:
            media_request = requests.get(url)
        except requests.exceptions.ConnectionError:
            logger.info('There was an error connecting to the api. ')
        except requests.exceptions.HTTPError:
            logger.info('Invalid HTTP response received. ')
        except requests.exceptions.Timeout:
            logger.info('The connection to the api timed out. ')
        except requests.exceptions.TooManyRedirects:
            logger.info('There have been too many redirects. ')
        if 'status_code' in media_request.json():
            if media_request.json().get('status_code') == 7:
                raise Exception(
                    'Error: ',
                    media_request.json().get('status_message')
                )
        return media_request.json()

    def __str__(self):
        if self.media_type == 'series':
            return ('{} (TV Show)'.format(self.title))
        elif self.media_type == 'episode':
            season_label = ' S0' if self.season < 10 else ' S'
            episode_label = 'E0' if self.episode < 10 else 'E'
            result_text = '{} {}{}{}{}'.format(
                self.tv_show.title,
                season_label,
                self.season,
                episode_label,
                self.episode)
            return (result_text)
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
    media_item = models.OneToOneField(
        MediaItem,
        related_name='media_request',
        on_delete=models.CASCADE,
        unique=True)
    requested_by = models.ForeignKey(
        'auth.User', related_name="+", on_delete=models.CASCADE)
    datetime_requested = models.DateTimeField(auto_now_add=True)
    completed_by = models.ForeignKey(
        'auth.User',
        related_name="+",
        null=True, blank=True,
        on_delete=models.CASCADE)
    datetime_completed = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(
        'auth.User',
        related_name="+",
        null=True,
        blank=True,
        on_delete=models.CASCADE)
    datetime_approved = models.DateTimeField(null=True, blank=True)
    rejected_by = models.ForeignKey(
        'auth.User',
        related_name="+",
        null=True,
        blank=True,
        on_delete=models.CASCADE)
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
        self.datetime_completed = timezone.localtime(timezone.now())
        self.save()

    def approve(self, approved_by):
        self.status = 'A'
        self.approved_by = approved_by
        self.datetime_approved = timezone.localtime(timezone.now())
        self.save()

    def reject(self, rejected_by):
        self.status = 'R'
        self.rejected_by = rejected_by
        self.datetime_rejected = timezone.localtime(timezone.now())
        self.save()

    def __str__(self):
        text = '{} by {} {}'.format(
            self.media_item,
            self.requested_by.first_name,
            self.requested_by.last_name)
        return text
