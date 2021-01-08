from django.db import models


# do we need other imports?
# file pathes?

# default values?
# allow null/empty?

# on_delete behaviour


# __str__ behaviour

# can't this metadata just be pulled from the track?
# why are we storing it in the database?






class Track(models.Model):
    title = models.CharField(max_length=100)
    artist = models.ManyToManyField(Artist, on_delete=models.CASCADE)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    disc_number = models.IntegerField()
    track_number = models.IntegerField()
    release_date = models.DateField()
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    publisher
    composer

    length = models.DurationField()

    # by default django gives each model id = models.AutoField(primary_key=True)
    # this is a auto-incrementing primary key (use to get random song?)

    comments 
    file_format
    bitrate_mode
    lossless
    sample_rate
    bits_per_sample
    channels
    bitrate
    encoder
    encoder_settings
    md5_signature
    compression_ratio


    def __str__(self):
        return self.title 


class Album(models.Model):
    name = models.CharField(max_length=100)
    artist = models.ManyToManyField(Artist, on_delete=models.CASCADE)
    discs = models.IntegerField()
    tracks = models.IntegerField()

    catalog_num

    # album cover?

    def __str__(self):
        return self.name


class Artist(models.Model):
    name = models.CharField(max_length=100, default="Unknown")

    # artist picture?

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=100, default="Unknown")



class Collection(models.Model):
    # the same as all tracks
    # each user has one collection
    # the same as playlists but linked to a user
    owner
    editors
    viewers
    public


class User(models.Model): # rename
    username = models.CharField(max_length=32)

    # prof pic
    # what about passwords?
    # history
    # playmode (shuffle, repeat, songs in queue, songs to add to queue)



class Playlist(models.Model):
    name = models.CharField(max_length=100)
    date_created = models.DateTimeField()
    date_modified = models.DateTimeField()
    owner = models.ManyToManyField(User, on_delete=models.CASCADE) # change?
    viewer = models.ManyToManyField(User, on_delete=models.CASCADe) # change?
    is_public = models.BooleanField()

    # Thumbnail? (select from a track)


