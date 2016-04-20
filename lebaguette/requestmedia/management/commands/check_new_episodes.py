import requests

from django.core.management.base import BaseCommand

from .models import TVShow, TVShowSeason, TVShowEpisode


class Command(BaseCommand):
    def handle(self, *args, **options):
        active_shows = TVShow.objects.filter(show_completed=False)
        print(active_shows)
