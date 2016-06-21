import requests

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from requestmedia.models import MediaItem


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.get(username='cronjob')
        active_shows = MediaItem.objects.filter(
            media_type='series',
            media_completed=False)
        # loop active shows in db
        for show in active_shows:
            start_episode = 1
            start_season = 1
            # add missing seasons from api
            latest_episode = show.get_latest_episode()
            if latest_episode:
                start_episode = latest_episode.episode
                start_season = latest_episode.season
            show.create_new_episodes(start_episode, start_season, user)

    def check_and_add_missing_seasons(self, show):
        db_seasons = TVShowSeason.objects.filter(
            tv_show=show).values_list('season_number', flat=True)
        seasons_numbers_from_api = self.get_all_seasons_numbers_from_api(show)
        for api_season_number in seasons_numbers_from_api:
            if api_season_number not in db_seasons:
                tv_show_season = TVShowSeason.create(
                    tv_show=show,
                    season_number=api_season_number)
                tv_show_season.save()
        return

    def get_all_seasons_numbers_from_api(self, show):
        seasons_numbers = []
        season = 1
        request = self.get_season_from_api(show.imdb_id, season)
        if request.json()['Response'] == 'True':
            seasons_numbers = range(1, int(request.json()['totalSeasons'])+1)
        return seasons_numbers

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
        except requests.exceptions.HTTPError:
            print('Invalid HTTP response received. ')
        except requests.exceptions.Timeout:
            print('The connection to the api timed out. ')
        except requests.exceptions.TooManyRedirects:
            print('There have been too many redirects. ')
        return episodes_request
