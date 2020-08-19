from datetime import datetime
from io import BytesIO
from unittest import mock
import tempfile

from django.core.files import File
from django.test import TestCase
from PIL import Image

from .models import Album, Picture


class AlbumModelTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.album = Album(name='My album', start_date=datetime.now())
        cls.album.save()
        super().setUpClass()

    @staticmethod
    def get_image_file(name='test.png', ext='png', size=(50, 50), color=(256, 0, 0)):
        file_obj = BytesIO()
        image = Image.new("RGBA", size=size, color=color)
        image.save(file_obj, ext)
        file_obj.seek(0)
        return File(file_obj, name=name)

    def add_n_pictures_to_album(self, nb_pictures):
        list_pictures = []
        with tempfile.TemporaryDirectory() as temp_dir:
            with self.settings(MEDIA_ROOT=temp_dir):
                for _ in range(nb_pictures):
                    pic = Picture(album=self.album, path=self.get_image_file())
                    pic.save()
                    list_pictures.append(pic)
        return list_pictures

    def test_get_pictures(self):
        self.assertEqual(self.album.get_pictures(), [])
        list_pictures = self.add_n_pictures_to_album(3)
        self.assertCountEqual(self.album.get_pictures(), list_pictures)

    def test_get_random_picture(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            with self.settings(MEDIA_ROOT=temp_dir):
                for _ in range(3):
                    pic = Picture(album=self.album, path=self.get_image_file())
                    pic.save()
            with mock.patch('apps.core.models.choice', return_value=pic.id):
                self.assertEqual(self.album.get_random_picture(), pic.path.url)

    def test_save(self):
        self.add_n_pictures_to_album(3)
        self.assertFalse(self.album.is_protected)
        for pic in self.album.get_pictures():
            self.assertFalse(pic.is_protected)
        self.album.is_protected = True
        self.album.save()
        self.assertTrue(self.album.is_protected)
        for pic in self.album.get_pictures():
            self.assertTrue(pic.is_protected)

    @mock.patch('apps.core.models.uuid.uuid4', return_value='595c87a1-2617-4ea8-823b-5af00697d9e2')
    def test_add_uuid(self, _):
        self.assertIsNone(self.album.uuid)
        self.album.add_uuid()
        self.assertEqual(self.album.uuid, '595c87a1-2617-4ea8-823b-5af00697d9e2')
