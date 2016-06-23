import requests

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from requestmedia.models import MediaItem


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.get(username='cronjob')
        active_shows = MediaItem.objects.filter(
            media_type='series',
            media_completed=False).exclude(media_request__status='N').exclude(media_request__status='R')
        # loop active shows in db
        for show in active_shows:
            start_episode = 0
            start_season = 1
            # add missing seasons from api
            latest_episode = show.get_latest_episode()
            if latest_episode:
                start_episode = latest_episode.episode
                start_season = latest_episode.season
            show.create_new_episodes(
                start_episode,
                start_season,
                user,
                'A')
