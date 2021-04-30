from django.db import models
from django.contrib.auth.models import User



# Possible next app to watch file and add to database



# Create your models here.

# only the owner has edit pems (might want to change in future)

# add way to make everything public and set every you add to public automatically

# basiclly folders
# will need to figure out how to make sure on correct folder (ie two subfolders with disc 1 and 2)

# add play everything in a folder




class Album(models.Model):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_albums')
    image = models.ImageField(upload_to='album_images', default='default_album.jpg')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name', 'id']


class Artist(models.Model):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_artists')
    image = models.ImageField(upload_to='artist_images', default='default_artist.jpg')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name', 'id']


class Genre(models.Model):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_genres')
    image = models.ImageField(upload_to='genre_images', default='default_genre.png')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name', 'id']


class Track(models.Model):
    title = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_tracks')
    # tie album with album song num in album 
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
    cover = models.ImageField(upload_to='track_images', default='default_track.jpg')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title', 'id'] 



class Playlist(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_playlists')
    public = models.BooleanField(default=False)
    name = models.CharField(max_length=200)
#       tracks = models.ManyToManyField(
#               Track,
#               related_name='playlist_tracks'
#       )
#       # add genre/album/artist/folder to playlist ?
#       # if added fields for genre/album/artist/folder how to deal with overlapping tracks ?

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name', 'id'] 


class Folder(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_folders')
    path = models.FileField()
