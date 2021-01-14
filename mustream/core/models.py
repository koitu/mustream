from django.db import models


# do we need other imports?
# file pathes?

# default values?
# allow null/empty?

# on_delete behaviour


# __str__ behaviour

# can't this metadata just be pulled from the track?
# why are we storing it in the database?


# ImageField requires pillow library







class Track(models.Model):
    location = models.FileField(upload_to=track_path) # ???

    title = models.CharField(max_length=100)
    artist = models.ManyToManyField(Artist, on_delete=models.CASCADE)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    disc_number = models.IntegerField()
    track_number = models.IntegerField()
    release_date = models.DateField()
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    # default should be non or null
    publisher = models.CharField(max_length=100)
    composer = models.CharField(max_length=100)

    length = models.DurationField()
    # length = models.DurationField(default=timedelta(seconds=0))

    # by default django gives each model id = models.AutoField(primary_key=True)
    # this is a auto-incrementing primary key (use to get random song?)

    history = ManyToManyField(History) # multiple tracks can belong to multiple historys (order?)

    metadata = OneToOneField(MetaData)

    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    playlists = models.ManyToManyField(Playlist)

    def __str__(self):
        return self.title 






class MetaData(models.Model):
    # does this actually need to be stored in the database???
    comments = TextField(
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





class MuUser(models.Model): # rename
    username = models.CharField(max_length=32)

    profile_picture = models.ImageField(max_length=100) # add limit for file size?

    history = models.OneToOneField(History)

    # what about passwords?
    # history
    # playmode (shuffle, repeat, songs in queue, songs to add to queue)





class History(models.Model):






class Playlist(models.Model):
    name = models.CharField(max_length=100)
    date_created = models.DateTimeField()
    date_modified = models.DateTimeField()
    owner = models.ManyToManyField(MuUser, on_delete=models.CASCADE) # change?
    viewer = models.ManyToManyField(MuUser, on_delete=models.CASCADe) # change?
    is_public = models.BooleanField()
    thumbnail = models.ImageField(max_length=100) # max_length is chars for the file name

    # thumbnail_src = DefaultStaticImageField(upload_to=album_thumbnail_path, default_image_path='empty-track.png')


