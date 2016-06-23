from django.test import TestCase
from django.core.management import call_command

from requestmedia.models import TVShow, TVShowSeason, TVShowEpisode


class CommandsTest(TestCase):

    def create_shows(self):
        call_command(
            'loaddata', 'tv_shows',
            verbosity=0)

    def test_create_seasons_and_episodes(self):
        self.create_shows()
        self.assertEqual(len(TVShow.objects.all()), 3)
        call_command('check_new_episodes')
        self.assertTrue(TVShowSeason.objects.all().exists())
        self.assertTrue(TVShowEpisode.objects.all().exists())

    def test_call_with_no_shows(self):
        call_command('check_new_episodes')
        self.assertEqual(len(TVShow.objects.all()), 0)

    def test_create_episodes_for_completed_season(self):
        self.create_shows()
        tv_show = TVShow.objects.get(id=1)
        tv_show_season = TVShowSeason.create(
            tv_show=tv_show,
            season_number=1)
        tv_show_season.season_completed = True
        tv_show_season.save()
        call_command('check_new_episodes')
        tv_show_episodes = TVShowEpisode.objects.filter(season=tv_show_season)
        self.assertFalse(tv_show_episodes.exists())

    def test_delete_first_season_and_recreate_it(self):
        self.create_shows()
        call_command('check_new_episodes')
        tv_show = TVShow.objects.get(id=1)
        tv_show_season_one = TVShowSeason.objects.get(
                                tv_show=tv_show,
                                season_number=1)
        tv_show_season_one.delete()
        self.assertFalse(TVShowSeason.objects.filter(
            tv_show=tv_show,
            season_number=1).exists())
        call_command('check_new_episodes')
        tv_show_season_one = TVShowSeason.objects.filter(
            tv_show=tv_show,
            season_number=1)
        self.assertTrue(tv_show_season_one.exists())
        tv_show_season_one_episodes = TVShowEpisode.objects.filter(
            season=tv_show_season_one)
        self.assertTrue(tv_show_season_one_episodes.exists())

    def test_delete_episodes_and_recreate_them(self):
        self.create_shows()
        call_command('check_new_episodes')
        tv_show = TVShow.objects.get(id=1)
        tv_show_season_one = TVShowSeason.objects.get(
                                tv_show=tv_show,
                                season_number=1)
        tv_show_episode_one = TVShowEpisode.objects.get(
                                season=tv_show_season_one,
                                episode_number=1)
        tv_show_episode_one.delete()
        call_command('check_new_episodes')
        tv_show_episode_one = TVShowEpisode.objects.filter(
                                season=tv_show_season_one,
                                episode_number=1)
        self.assertTrue(tv_show_episode_one.exists())
