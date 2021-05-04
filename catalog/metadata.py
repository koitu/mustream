from catalog.models import Album, Artist, Genre, Track
from django.db import models
import audio_metadata
from django.dispatch import receiver


# django-cleanup will handle image cleanup


@receiver(models.signals.post_delete, sender=Track)
def delete_when_empty(sender, instance, **kwargs):
    try:
        if instance.album.album_tracks.count() == 0:
            instance.album.delete()
    except:
        pass

    try:
        if instance.artist.artist_tracks.count() == 0:
            instance.artist.delete()
    except:
        pass

    try:
        if instance.genre.genre_tracks.count() == 0:
            instance.genre.delete()
    except:
        pass



def get_or_create(queryset, name, model, owner):
    if name:
        try:
            obj = queryset.get(name=name)
        except:
            obj = model(name=name, owner=owner)
            album.save()
        finally:
            return obj
    return None



def create_track_from_file(file, owner):
    if file.size > 2e8 # 200 mb
        return None

    filename, ext = os.path.splitext(os.path.basename(file.name))
    track = Track(title=filename, owner=owner, audio=file)
    tempfile = TempFile(file=file)
    tempfile.save()

    try:
        metadata = audio_metadata.load(track.tempfile.file)
    except:
        tempfile.delete()
        if ext in ('.flac', '.mp3', '.aac', '.ogg', '.opus', '.wav'):
            return track
        return None
    else:
        tempfile.delete()

    try:
        if metadata.tags.title:
            title = metadata.tags.title 
    except:
        pass
    try:
        track.album = get_or_create(queryset=owner.user_albums.all(),
                name=metadata.tags.album, model=Album, owner=owner)
        # also need to get track_number and disc number
        # need to deal if adding file has the same name, artist, album (append id?)
        # if track.album is using default_image and track has a image then album.image=track.image
    except:
        pass
    try:
        track.artist = get_or_create(queryset=owner.user_artists.all(),
                name=metadata.tags.artist, model=Artist, owner=owner)
    except:
        pass
    try:
        track.genre = get_or_create(queryset=owner.user_genres.all(),
                name=metadata.tags.genre, model=Genre, owner=owner)
    except:
        pass
    try:
        duration = metadata.streaminfo.duration.split(':')
        track.duration = datetime.timedelta(minutes=duration[0], seconds=duration[1])
    except:
        pass

    return track






# def reset_db(User)
#   delete current db ? # is it faster to compare diff and add/rm tracks/stuff or just wipe and genreate from files
#   for folder in user.userfolders
#       scan_folder(folder)


