from random import choice

from django.db import models


class Album(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    parent_album = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name

    def get_pictures(self):
        """Get the pictures of the current album
        """
        return Picture.objects.filter(album__id=self.id)

    def get_random_picture(self):
        """Get one random picture from the album. Used as the thumbnail of the album when displaying the list of albums
        """
        pks = self.get_pictures().values_list('pk', flat=True)
        random_pk = choice(pks)
        random_pic = Picture.objects.get(pk=random_pk)
        return random_pic.path.url


class Picture(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    path = models.ImageField()
