from django.db import models


class Album(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    parent_album = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name


class Picture(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    path = models.ImageField()
