from django.db import models

# Create your models here.

# want to originize by folder as well

class Album(models.Model):
    name = models.CharField(max_length=200, primary_key=True)
    # picture

    def __str__(self):
        return self.name


class Artist(models.Model):
    name = models.CharField(max_length=200, primary_key=True)
    # picture 

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=200, primary_key=True)

    def __str__(self):
        return self.name


class Track(models.Model):
    title = models.CharField(max_length=200, primary_key=True)
    album = models.ForeignKey(
            Album, 
            blank=True, 
            null=True, 
            on_delete=models.CASCADE,
            related_name='album_tracks'
    )
    artist = models.ForeignKey(
            Artist, 
            blank=True, 
            null=True, 
            on_delete=models.CASCADE,
            related_name='artist_tracks'
    )
    genre = models.ForeignKey(
            Genre, 
            blank=True, 
            null=True, 
            on_delete=models.CASCADE,
            related_name='artist_tracks'
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id'] 


class Playlist(models.Model):
    name = models.CharField(max_length=200)
    tracks = models.ManyToManyField(
            Track,
            related_name='playlist_tracks'
    )

    def __str__(self):
        return self.name
