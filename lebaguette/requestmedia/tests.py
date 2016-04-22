from django.test import TestCase
from django.core.management import call_command

from requestmedia.models import TVShow, TVShowSeason, TVShowEpisode


class CommandsTest(TestCase):
    def test_get_shows_data(self):
        call_command(
            'loaddata', 'tv_shows',
            verbosity=0)
        self.assertEqual(len(TVShow.objects.all()), 3)
        call_command('check_new_episodes')
        self.assertTrue(TVShowEpisode.objects.all().exists())

    def test_call_with_no_shows(self):
        call_command('check_new_episodes')
        self.assertEqual(len(TVShow.objects.all()), 0)

    def test_create_episodes_for_completed_season(self):
        call_command(
            'loaddata', 'tv_shows',
            verbosity=0)
        tv_show = TVShow.objects.get(id=1)
        tv_show_season = TVShowSeason.create(
            tv_show=tv_show,
            season_number=1)
        tv_show_season.season_completed = True
        tv_show_season.save()
        call_command('check_new_episodes')
        tv_show_episodes = TVShowEpisode.objects.filter(season=tv_show_season)
        self.assertFalse(tv_show_episodes.exists())
