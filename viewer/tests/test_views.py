from datetime import datetime

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from viewer.models import Album, Picture


class ViewerViewsTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = Client()
        cls.album_1 = Album(name='My album', start_date=datetime.now())
        cls.album_1.save()
        cls.album_2 = Album(name='My protected album', start_date=datetime.now(), is_protected=True)
        cls.album_2.save()
        user = User.objects.create_user(
            'user',
            email='user@domain.com',
            password='password'
        )
        user.save()
        super().setUpClass()

    def setUp(self):
        # Make sure the user is logged out, even if the test fails
        self.client.logout()

    def test_home_view_get(self):
        response = self.client.get(reverse('viewer:home'))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        self.assertCountEqual(
            list(response.context['albums']),
            list(Album.objects.filter(is_protected=False))
        )

        self.client.login(username='user', password='password')
        response = self.client.get(reverse('viewer:home'))
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(
            list(response.context['albums']),
            list(Album.objects.all())
        )

    def test_album_view_get(self):
        response = self.client.get(reverse('viewer:album_id', kwargs={'id_album': self.album_1.id}))
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['album'], self.album_1)

        self.album_1.add_uuid()
        response = self.client.get(reverse('viewer:album_uuid', kwargs={'uuid': self.album_1.uuid}))
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['album'], self.album_1)

        response = self.client.get(reverse('viewer:album_id', kwargs={'id_album': self.album_2.id}))
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        self.assertEqual(response.status_code, 403)

        self.album_2.add_uuid()
        response = self.client.get(reverse('viewer:album_uuid', kwargs={'uuid': self.album_2.uuid}))
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['album'], self.album_2)

        self.client.login(username='user', password='password')
        response = self.client.get(reverse('viewer:album_id', kwargs={'id_album': self.album_2.id}))
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['album'], self.album_2)
