from django.db import models
from django.contrib.auth.models import User


# formats: mp3, opus, aac, flac, wav, .ogg/oga/mogg, (? .webm, .m4a, .m4b, .m4p, .ape)


# Possible next app to watch file and add to database



# Create your models here.

# only the owner has edit pems (might want to change in future)

# add way to make everything public and set every you add to public automatically

# basiclly folders
# will need to figure out how to make sure on correct folder (ie two subfolders with disc 1 and 2)

# add play everything in a folder
class Album(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_albums')
    public = models.BooleanField(default=False)
    name = models.CharField(max_length=200)
    # picture

    def __str__(self):
        return self.name


class Artist(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_artists')
    public = models.BooleanField(default=False)
    name = models.CharField(max_length=200)
    # picture 

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Track(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_tracks')
    public = models.BooleanField(default=False)
    force_private = models.BooleanField(default=False)
    title = models.CharField(max_length=200)
    # tie album with song num in album (backup will just be alpha order)
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
            on_delete=models.CADCADE,
            related_name='artist_tracks'
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title'] 


class Playlist(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_playlists')
    public = models.BooleanField(default=False)
    name = models.CharField(max_length=200)
    tracks = models.ManyToManyField(
            Track,
            related_name='playlist_tracks'
    )

    def __str__(self):
        return self.name
