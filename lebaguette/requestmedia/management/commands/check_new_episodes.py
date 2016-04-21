import requests

from django.core.management.base import BaseCommand

from requestmedia.models import TVShow, TVShowSeason, TVShowEpisode


class Command(BaseCommand):
    def handle(self, *args, **options):
        active_shows = TVShow.objects.filter(show_completed=False)
        self.get_new_episodes(active_shows)

    def get_new_episodes(self, active_shows):
        # loop shows in db
        for show in active_shows:
            season = 1
            request = self.get_season_episodes(show.imdb_id, season)
            # loop episodes from omdb api
            while request.json()['Response'] == 'True':
                if TVShowSeason.objects.filter(tv_show=show,
                                               season_number=season).exists():
                    print('success')
                else:
                    tv_show_season = TVShowSeason.create(tv_show=show,
                                                         season_number=season)
                    tv_show_season.save()
                season += 1
                request = self.get_season_episodes(show.imdb_id, season)

    def get_season_episodes(self, imdb_id, season):
        try:
            episodes = requests.get('http://www.omdbapi.com/?i=' +
                                    imdb_id +
                                    '&Season=' +
                                    str(season) +
                                    '&plot=short&r=json')
        except requests.exceptions.ConnectionError, e:
            print('There was an error connecting to the api. ', e)
        except request.exceptions.HTTPError, e:
            print('Invalid HTTP response received. ', e)
        except request.exceptions.Timeout, e:
            print('The connection to the api timed out. ', e)
        except request.exceptions.TooManyRedirects, e:
            print('There have been too many redirects. ', e)
        return episodes
