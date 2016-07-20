from django.test import TestCase
from django.core.management import call_command
from django.test.client import Client

from requestmedia.models import MediaItem, Request


class CommandsTest(TestCase):
    fixtures = [
        'home/fixtures/users_data',
        'requestmedia/fixtures/media_items']

    def test_add_ajax_filter(self):
        self.client = Client()
        self.client.login(username='admin', password='admin1234')
        response = self.client.post(
            '/requestmedia/add/',
            {'imdb_id': 'tt4158110tt2357547'})
        self.assertEqual(response.status_code, 403)

    def test_add_request(self):
        self.client = Client()
        self.client.login(username='admin', password='admin1234')
        response = self.client.post(
            '/requestmedia/add/',
            {'imdb_id': 'tt4158110tt2357547'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(MediaItem.objects.filter(imdb_id='tt4158110').exists())
        media_item = MediaItem.objects.get(imdb_id='tt4158110')
        self.assertTrue(Request.objects.filter(media_item=media_item).exists())
        self.assertTrue(MediaItem.objects.filter(imdb_id='tt2357547').exists())
        media_item = MediaItem.objects.get(imdb_id='tt2357547')
        self.assertTrue(Request.objects.filter(media_item=media_item).exists())

    def test_complete_ajax_filter(self):
        self.client = Client()
        self.client.login(username='admin', password='admin1234')
        response = self.client.post(
            '/requestmedia/complete/',
            {'itemid': '1179'})
        self.assertEqual(response.status_code, 403)

    def test_complete_reqeust(self):
        self.client = Client()
        self.client.login(username='admin', password='admin1234')
        response = self.client.post(
            '/requestmedia/complete/',
            {'itemid': '1179'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        request_item = Request.objects.get(id=1179)
        self.assertEqual(request_item.status, 'C')

    def test_approve_ajax_filter(self):
        self.client = Client()
        self.client.login(username='admin', password='admin1234')
        response = self.client.post(
            '/requestmedia/approve/',
            {'itemid': '1179'})
        self.assertEqual(response.status_code, 403)

    def test_approve_request(self):
        self.client = Client()
        self.client.login(username='admin', password='admin1234')
        response = self.client.post(
            '/requestmedia/approve/',
            {'itemid': '1179'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        request_item = Request.objects.get(id=1179)
        self.assertEqual(request_item.status, 'A')

    def test_reject_request(self):
        self.client = Client()
        self.client.login(username='admin', password='admin1234')
        response = self.client.post(
            '/requestmedia/reject/',
            {'itemid': '1179'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        request_item = Request.objects.get(id=1179)
        self.assertEqual(request_item.status, 'R')
