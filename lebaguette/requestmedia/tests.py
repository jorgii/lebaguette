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

    
