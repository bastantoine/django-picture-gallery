from random import choice
import uuid

from django.db import models


class Album(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    parent_album = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    is_protected = models.BooleanField(default=False)
    uuid = models.UUIDField(blank=True, null=True)

    def __str__(self):
        return self.name

    def get_pictures(self):
        """Get the pictures of the current album or an empty list if there's no pictures
        """
        all_pictures = Picture.objects.filter(album__id=self.id)
        return all_pictures if all_pictures else []

    def get_random_picture(self):
        """Get one random picture from the album. Used as the thumbnail of the album when displaying the list of albums
        """
        all_pictures = self.get_pictures()
        if not all_pictures:
            return ''
        pks = all_pictures.values_list('pk', flat=True)
        random_pk = choice(pks)
        random_pic = Picture.objects.get(pk=random_pk)
        return random_pic.path.url

    def add_uuid(self):
        if not self.uuid:
            self.uuid = uuid.uuid4()
            self.save()

    def save(self, *args, **kwargs):
        """Overload of the default save method. Sets the protection flag of all
        the pictures of the album to the same value of the flag of the album
        """
        for picture in self.get_pictures():
            picture.is_protected = self.is_protected
            picture.save()
        super().save(*args, **kwargs)

    def update(self, **kwargs):
        # Make sure we don't update the id
        kwargs.pop('id', None)
        kwargs.pop('pk', None)
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()


class Picture(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    path = models.ImageField()
    is_protected = models.BooleanField(default=False)
