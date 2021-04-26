from datetime import timedelta
from django.db import models
from django.contrib.auth.models import User


# do we need other imports?
# file pathes?

# default values? (images and other stuff)
# image update_to
# allow null/empty?

# ImageField requires pillow library


class Profile(models.Model): 
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(max_length=100) # add limit for file size?
    # history and playstate will be set on instance to instance basis

# might not need to collections
# how to give access to collection then?
class Collection(models.Model):
    # the same as all tracks
    # each user has one collection
    # the same as playlists but linked to a user
    owner = models.OneToOneField(User, on_delete=models.CASCADE) # ??????????
#    editors = models.ManyToManyField(User, blank=True)
#    viewers = models.ManyToManyField(User, blank=True)
    public = models.BooleanField(default=False)


class Playlist(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField() # update_to=''
    # thumbnail_src = DefaultStaticImageField(upload_to=album_thumbnail_path, default_image_path='empty-track.png')
    date_created = models.DateTimeField()
    date_modified = models.DateTimeField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE) 
#    editors = models.ManyToManyField(User, blank=True)
#    viewers = models.ManyToManyField(User, blank=True)
    public = models.BooleanField(default=False)


class Artist(models.Model):
    name = models.CharField(max_length=100, default="Unknown")
    image = models.ImageField() # update_to=''
    comments = models.TextField(max_length=500)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Album(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField() # update_to=''
    artist = models.ManyToManyField(Artist, blank=True)
    discs = models.IntegerField()
    tracks = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Genre(models.Model):
    name = models.CharField(max_length=100, default="Unknown")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


# metadata can be taken directly from file
class Track(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    location = models.FileField() # update_to=''
    image = models.ImageField() # update_to=''
    artist = models.ManyToManyField(Artist, blank=True)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, blank=True)
    genre = models.ForeignKey(Genre, on_delete=models.RESTRICT, blank=True) # should not be able to delete by genre
    length = models.DurationField(default=timedelta(seconds=0))
    release_date = models.DateField()
    disc_number = models.IntegerField()
    track_number = models.IntegerField()
    playlists = models.ManyToManyField(Playlist)

    def __str__(self):
        return self.title 

    class Meta:
        ordering = ['title']