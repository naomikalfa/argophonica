from django.db import models
from django_extensions.db.fields import AutoSlugField


class Artist(models.Model):

    artist = models.TextField(blank=False, null=False, unique=True)
    albums = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.artist


class Album(models.Model):

    title = models.TextField(blank=False, null=False)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    release_date = models.TextField(blank=True, null=True)
    genre = models.TextField(blank=True, null=True)
    number_tracks = models.TextField(blank=True, null=True)
    track_list = models.TextField(blank=True, null=True)
    length = models.TextField(blank=True, null=True)
    file_type = models.TextField(blank=True, null=True)
    artwork_file = models.ImageField(blank=True, null=True, max_length=500)
    artwork_link = models.TextField(blank=True, null=True, max_length=500)
    notes = models.TextField(blank=True, null=True)
    slug = AutoSlugField(null=True, default=None, unique=True, max_length=500, populate_from='title')

    def __str__(self):
        return self.title


class Track(models.Model):

    title = models.TextField(blank=False, null=False)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    artist = models.TextField(blank=True, null=True)
    length = models.TextField(blank=True, null=True)
    track_number = models.PositiveIntegerField(blank=True, null=True)
    audio_file = models.FileField(blank=True, null=True, max_length=500)
    audio_link = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title
