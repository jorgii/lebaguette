from django.test import TestCase
from django.core.management import call_command
from django.test.client import Client

from requestmedia.models import MediaItem, Request


class CommandsTest(TestCase):
    fixtures = ['home/fixtures/users_data', 'home/fixtures/messages']

    def test_add_request(self):
        self.client = Client()
        self.client.login(username='admin', password='admin1234')
        response = self.client.post(
            '/requestmedia/add/',
            {'imdb_id': 'tt3107288'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(MediaItem.objects.filter(imdb_id='tt3107288').exists())
        media_item = MediaItem.objects.get(imdb_id='tt3107288')
        self.assertTrue(Request.objects.filter(media_item=media_item).exists())
