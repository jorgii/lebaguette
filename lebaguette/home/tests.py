from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse


class HomeTest(TestCase):
    fixtures = ['home/fixtures/users_data', 'home/fixtures/messages']

    def setUp(self):
        self.client = Client()
        self.admin = User.objects.get(pk=1)
        self.user = User.objects.get(pk=2)

    def user_post_data(self, user):
        return dict(username=user.username,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    email=user.email)

    def test_view_login_get(self):
        url = reverse('login',)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_view_login_post(self):
        url = reverse('login',)
        response = self.client.post(url, dict(username='test',
                                              password='pasta1234'))
        self.assertEqual(response.status_code, 302)

    def test_view_profile_get(self):
        self.client.login(username='test', password='pasta1234')
        url = reverse('profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_edit_profile_post(self):
        self.client.login(username='test', password='pasta1234')
        url = reverse('profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        user = response.context['user']
        data = self.user_post_data(user)
        data['username'] = 'newusername'
        data['first_name'] = 'changed firstname'
        data['last_name'] = 'changed lastname'
        data['email'] = 'asd@asd.asd'
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, data['username'])
        self.assertEqual(self.user.first_name, data['first_name'])
        self.assertEqual(self.user.last_name, data['last_name'])
        self.assertEqual(self.user.email, data['email'])

    def test_logout(self):
        self.client.login(username='test', password='pasta1234')
        url = reverse('logout')
        response = self.client.get(url)
        expected_url = reverse('login')
        self.assertRedirects(response, expected_url,
                             status_code=302,
                             target_status_code=200)

    def test_view_home_page(self):
        self.client.login(username='test', password='pasta1234')
        url = reverse('home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_add_message_as_non_staff(self):
        self.client.login(username='test', password='pasta1234')
        url = reverse('home')
        data = {}
        data['message'] = 'Trying to post message'
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)

    def test_add_message_as_staff(self):
        self.client.login(username='admin', password='admin1234')
        url = reverse('home')
        data = {}
        data['message'] = 'Trying to post message'
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
