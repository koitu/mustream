from django.db import models
from django.contrib.auth.models import User



# Possible next app to watch file and add to database



# Create your models here.

# only the owner has edit pems (might want to change in future)

# add way to make everything public and set every you add to public automatically

# basiclly folders
# will need to figure out how to make sure on correct folder (ie two subfolders with disc 1 and 2)

# add play everything in a folder


def album_path(instance, filename):
    return '{0}/album_images/{1}'.format(instance.owner.get_username(), filename)

class Album(models.Model):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_albums')
    image = models.ImageField(upload_to=album_path, default='default_album.jpg')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name', 'id']


def artist_path(instance, filename):
    return '{0}/artist_images/{1}'.format(instance.owner.get_username(), filename)

class Artist(models.Model):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_artists')
    image = models.ImageField(upload_to=artist_path, default='default_artist.jpg')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name', 'id']


def genre_path(instance, filename):
    return '{0}/genre_images/{1}'.format(instance.owner.get_username(), filename)

class Genre(models.Model):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_genres')
    image = models.ImageField(upload_to=genre_path, default='default_genre.png')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name', 'id']


def track_path(instance, filename):
    artist = instance.artist if instance.artist is not None else "unknown_artist"
    album = instance.album if instance.album is not None else "unknown_album"
    # album can have more than one artist
    return '{0}/{1}/{2}/{3}'.format(instance.owner.get_username(), artist, album, filename)

class Track(models.Model):
    title = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_tracks')
    image = models.ImageField(upload_to=track_path, default='default_track.jpg')
    audio = models.FileField(upload_to=track_path)

    album_track_number = models.IntegerField(default=0)
    album = models.ForeignKey(Album, 
            blank=True, 
            null=True, 
            on_delete=models.CASCADE,
            related_name='album_tracks')
    artist = models.ForeignKey(Artist, 
            blank=True, 
            null=True, 
            on_delete=models.CASCADE,
            related_name='artist_tracks')
    genre = models.ForeignKey(Genre, 
            blank=True, 
            null=True, 
            on_delete=models.CASCADE,
            related_name='artist_tracks')
    # in the future could extend to support multiple artists, genres, albums

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


# only staff can modify (normal users can updatedb to add tracks to db but only stuff can add other folders)
class Folder(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_folders')
    path = models.FileField()
