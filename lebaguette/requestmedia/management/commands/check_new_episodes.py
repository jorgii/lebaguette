import requests
import time
from datetime import datetime, date

from django.core.management.base import BaseCommand

from requestmedia.models import TVShow, TVShowSeason, TVShowEpisode


class Command(BaseCommand):
    def handle(self, *args, **options):
        start_time = time.time()
        active_shows = TVShow.objects.filter(show_completed=False)
        self.get_new_episodes(active_shows)
        print("The operation took me %s seconds" % (time.time() - start_time))

    def get_new_episodes(self, active_shows):
        # loop active shows in db
        for show in active_shows:
            print('Start working on ', show.title)
            # get the latest active season
            if TVShowSeason.objects.filter(tv_show=show).exists():
                season = TVShowSeason.objects.filter(
                    tv_show=show,
                    season_completed=False).order_by(
                        '-season_number')[0].season_number
            else:
                season = 1
            request = self.get_season_episodes(show.imdb_id, season)
            # loop seasons from omdb api
            while request.json()['Response'] == 'True':
                if not TVShowSeason.objects.filter(
                        tv_show=show,
                        season_number=season).exists():
                    # Create tv show season if non existent
                    tv_show_season = TVShowSeason.create(tv_show=show,
                                                         season_number=season)
                    tv_show_season.save()
                    print('Added ', show.title, '; Season ', season)
                # loop through episodes
                for episode in request.json()['Episodes']:
                    if TVShowEpisode.objects.filter(
                            episode_number=episode['Episode'],
                            season=TVShowSeason.objects.get(
                                tv_show=show,
                                season_number=season),
                            episode_imdbid=episode['imdbID']).exists():
                        pass
                    else:
                        # create non existent episodes that have already aired
                        if date.today() >= datetime.strptime(
                                episode['Released'],
                                '%Y-%m-%d').date():
                            tv_show_episode = TVShowEpisode.create(
                                season=TVShowSeason.objects.get(
                                    tv_show=show,
                                    season_number=season),
                                episode_title=episode['Title'],
                                episode_number=int(episode['Episode']),
                                episode_released=datetime.strptime(
                                    episode['Released'],
                                    '%Y-%m-%d').date(),
                                episode_imdbid=episode['imdbID'])
                            tv_show_episode.save()
                            print(
                                'Added episode ', episode['Episode'],
                                ' for Season ', season,
                                ' in tv show ', show.title)
                season += 1
                request = self.get_season_episodes(show.imdb_id, season)

    def get_season_episodes(self, imdb_id, season):
        try:
            episodes = requests.get('http://www.omdbapi.com/?i=' +
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
        return episodes
