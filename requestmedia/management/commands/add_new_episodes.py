import time
import logging

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from requestmedia.models import MediaItem


class Command(BaseCommand):
    def handle(self, *args, **options):
        logger = logging.getLogger('django.info')
        logger.info("Started working on TV Show episodes!")
        start_time = time.time()
        user = User.objects.get(username='cronjob')
        active_shows = MediaItem.objects.filter(
            media_type='series',
            media_completed=False).exclude(
            media_request__status='N').exclude(media_request__status='R')
        # loop active shows in db
        for show in active_shows:
            logger.info("Started working on {0}!".format(str(show)))
            start_episode = 0
            start_season = 1
            # add missing seasons from api
            latest_episode = show.get_latest_episode()
            if latest_episode:
                logger.info("Latest Episode: {0}".format(str(latest_episode)))
                start_episode = latest_episode.episode
                start_season = latest_episode.season
            show.create_new_episodes(
                start_episode,
                start_season,
                user,
                'A')
            logger.info("Finished working on {0}!".format(str(show)))
        execution_time = time.time() - start_time
        logger.info("Finished! Execution time: {0:0.2f} seconds!".format(
            execution_time))
