import requests
import time
from datetime import datetime, date

from django.core.management.base import BaseCommand

from requestmedia.models import TVShow, TVShowSeason, TVShowEpisode


class Command(BaseCommand):
    def handle(self, *args, **options):
        active_shows = TVShow.objects.filter(show_completed=False)
        self.get_new_episodes(active_shows)

    def get_new_episodes(self, active_shows):
        # loop active shows in db
        for show in active_shows:
            # add missing seasons from api
            self.check_and_add_missing_seasons(show)
            # loop active seasons in db and add missing episodes
            seasons = TVShowSeason.objects.filter(
                    tv_show=show,
                    season_completed=False)
            for season in seasons:
                episodes_request = self.get_season_from_api(
                    imdb_id=show.imdb_id,
                    season.season_number)
                show.create_episodes_from_json(
                    season,
                    episodes_request.json())

    def get_season_()

    def check_and_add_missing_seasons(self, show):
        db_seasons = TVShowSeason.objects.filter(
            tv_show=show).values_list('season_number', flat=True)
        seasons_from_api = self.get_all_seasons_from_api(show)
        for api_season in seasons_from_api:
            if api_season not in db_seasons:
                tv_show_season = TVShowSeason.create(
                    tv_show=show,
                    season_number=season)
                tv_show_season.save()
        return

    def get_all_seasons_from_api(self, show):
        seasons = []
        season = 1
        request = self.get_season_from_api(show.imdb_id, season)
        while request.json()['Response'] == 'True':
            seasons.append(season)
            season += 1
            request = self.get_season_from_api(show.imdb_id, season)

    def get_season_from_api(self, imdb_id, season):
        try:
            episodes_request = requests.get(
                'http://www.omdbapi.com/?i=' +
                imdb_id +
                '&Season=' +
                str(season) +
                '&plot=short&r=json')
        except requests.exceptions.ConnectionError:
            print('There was an error connecting to the api. ')
        except request.exceptions.HTTPError:
            print('Invalid HTTP response received. ')
        except request.exceptions.Timeout:
            print('The connection to the api timed out. ')
        except request.exceptions.TooManyRedirects:
            print('There have been too many redirects. ')
        return episodes_request
