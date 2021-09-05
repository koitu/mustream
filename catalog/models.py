import os

from django.db import models
from django.contrib.auth.models import User


# https://stackoverflow.com/questions/8332443/set-djangos-filefield-to-an-existing-file
def album_image_path(instance, filename):
    file, ext = os.path.splitext(os.path.basename(filename)) 
    track = instance.album_tracks.last()
    artist = track.artist if track.artist else "unknown_artist"
    album = track.album if track.album else "unknown_album"
    imagepath = '{0}/{1}/{2}/cover{3}'.format(instance.owner.username, artist, album, ext)
    instance.album_tracks.update(image=imagepath)
    return imagepath


class Album(models.Model):
    name = models.CharField(max_length=120)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_albums')
    image = models.ImageField(upload_to=album_image_path, default='default_album.png')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name', 'id']
        unique_together = ['name', 'owner']


def artist_image_path(instance, filename):
    file, ext = os.path.splitext(os.path.basename(filename))
    return '{0}/artist_images/{1}{2}'.format(instance.owner.username, instance.name, ext)


class Artist(models.Model):
    name = models.CharField(max_length=120)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_artists')
    image = models.ImageField(upload_to=artist_image_path, default='default_artist.png')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name', 'id']
        unique_together = ['name', 'owner']


def genre_image_path(instance, filename):
    file, ext = os.path.splitext(os.path.basename(filename))
    return '{0}/genre_images/{1}{2}'.format(instance.owner.username, instance.name, ext)


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


def track_image_path(instance, filename):
    artist = instance.artist if instance.artist else "unknown_artist"
    return '{0}/{1}/unknown_album/{2}'.format(instance.owner.username, artist, filename)


class Track(models.Model):
    title = models.CharField(max_length=120)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_tracks')
    audio = models.FileField(upload_to=track_path)  # track.audio.size will return filesize
    image = models.ImageField(upload_to=track_image_path, default='default_track.png')
    duration = models.DurationField(blank=True, null=True)
    album = models.ForeignKey(
        Album,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='album_tracks',
    )
    album_track_number = models.IntegerField(blank=True, null=True)
    album_total_tracks = models.IntegerField(blank=True, null=True)
    album_disc_number = models.IntegerField(blank=True, null=True)
    album_total_discs = models.IntegerField(blank=True, null=True)
    artist = models.ForeignKey(
        Artist,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='artist_tracks',
    )
    genre = models.ForeignKey(
        Genre,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='artist_tracks',
    )
    year = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title', 'id'] 
        unique_together = [
            ['title', 'owner'],
            ['album_track_number', 'album_disc_number', 'album'],
        ]


class Playlist(models.Model):
    name = models.CharField(max_length=120)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_playlists')
    public = models.BooleanField(default=False)
    tracks = models.ManyToManyField(
            Track,
            related_name='track_playlists',
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name', 'id'] 
        unique_together = ['name', 'owner']


def user_image_path(instance, filename):
    file, ext = os.path.splitext(os.path.basename(filename))
    return '{0}/user{1}'.format(instance.user.username, ext)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_settings', unique=True)
    image = models.ImageField(upload_to=user_image_path, default='default_user.png')
    shuffle = models.BooleanField(default=False)
    current_track = models.IntegerField()  # pk of the track
    # public or private (default is private) (public will generate a public playlist with all songs)
    # space used
    # space limit

# track_presave() signal check if within storage limit for user and return response is so
# else update space used

# register models into admin panel
# register(Album)
# register(Artist)
# register(Genre)
# register(Track)
# register(Playlist)
