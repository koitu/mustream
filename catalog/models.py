from django.db import models
from django.contrib.admin.site import register
from django.contrib.auth.models import User



def album_image_path(instance, filename):
    filename, ext = os.path.splitext(os.path.basename(filename))
    track = instance.album_tracks.first()
    artist = track.artist if track.artist else "unknown_artist"
    album = track.album if track.album else "unknown_album"
    imagepath = '{0}/{1}/{2}/cover{3}'.format(instance.owner.username, artist, album, ext)
    instance.album_tracks.update(image=imagepath)
    return imagepath

class Album(models.Model):
    name = models.CharField(max_length=120)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_albums')
    image = models.ImageField(upload_to=album_image_path, default='default_album.jpg')
    total_tracks = models.IntegerField(blank=True, null=True)
    total_discs= models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name', 'id']
        unique_together = ['name', 'owner']



def artist_image_path(instance, filename):
    return '{0}/artist_images/{1}-{2}'.format(instance.owner.username, instance.name, filename)

class Artist(models.Model):
    name = models.CharField(max_length=120)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_artists')
    image = models.ImageField(upload_to=artist_image_path, default='default_artist.jpg')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name', 'id']
        unique_together = ['name', 'owner']



def genre_image_path(instance, filename):
    return '{0}/genre_images/{1}-{2}'.format(instance.owner.username, instance.name, filename)

class Genre(models.Model):
    name = models.CharField(max_length=120)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_genres')
    image = models.ImageField(upload_to=genre_image_path, default='default_genre.png')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name', 'id']
        unique_together = ['name', 'owner']



def track_path(instance, filename):
    artist = instance.artist if instance.artist else "unknown_artist"
    album = instance.album if instance.album else "unknown_album"
    return '{0}/{1}/{2}/{3}'.format(instance.owner.username, artist, album, filename)

class Track(models.Model):
    title = models.CharField(max_length=120)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_tracks')
    audio = models.FileField(upload_to=track_path)
    image = models.ImageField(default='default_track.jpg')
    duration = models.DurationField(blank=True, null=True)
    album_track_number = models.IntegerField(blank=True, null=True)
    album_disc_number = models.IntegerField(blank=True, null=True)
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
    # year
    # date
    # filesize

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title', 'id'] 
        unique_together = [['title', 'owner'], ['album_track_number', 'album_disc_number', 'album']]



# TODO:

# play by folder (admin only)
class Playlist(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_playlists')
    public = models.BooleanField(default=False)
    name = models.CharField(max_length=120)
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
    # path = models.FileField() (correct field?)


def user_path(instance, filename):
    return '{0}/{1}'.format(instance.user.username, filename)

class UserSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_settings', unique=True)
    shuffle = models.BooleanField(default=False)
    image = models.ImageField(upload_to=user_path, default='default_user.jpg')
    # play mode (what genre, artist, album, or all was being played)
    # public or private (default is private) (public will generate a public playlist with all songs)
    # space used
    # space limit


# register models into admin panel
register(Album)
register(Artist)
register(Genre)
register(Track)
register(Playlist)
