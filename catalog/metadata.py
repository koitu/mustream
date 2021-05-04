from catalog.models import Album, Artist, Genre, Track
from django.db import models
import audio_metadata
from django.dispatch import receiver
from datetime import timedelta
import os


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
            obj.save()
        finally:
            return obj
    return None



def create_track_from_file(file, owner):
    # could move this block into views --------------------------
    if file.size > 2e8: # 200 mb is maxfilesize
        return None
    filename, ext = os.path.splitext(os.path.basename(file.name))
    track = Track(title=filename, owner=owner, audio=file)
    try:
        metadata = audio_metadata.load(file.temporary_file_path())
    except:
        if ext in ('.flac', '.mp3', '.aac', '.ogg', '.opus', '.wav'):
            return track
        return None
    # and rename this to apply_metadata(track, file, owner) ----
    # don't want to import audio_metadata into views tho

    try:
        if metadata.tags.title[0]:
            track.title = metadata.tags.title[0]
    except:
        pass

    try:
        track.album = get_or_create(queryset=owner.user_albums.all(),
                name=metadata.tags.album[0], model=Album, owner=owner)
        # also need to get track_number and disc number
        # num, total = metadat.tags.discnumber[0].split('/') 
        # sometimes metadata will use discnumber and disctotal
        # num, total = metadata.tags.discnumber[0], metadata.tags.disctotal[0]

        # need to deal if adding file has the same name, artist, album (append id?)
        # image?
        # if track.album is using default_image and track has a image then album.image=track.image
        # will also need to update this when track is deleted
    except:
        pass

    try:
        track.artist = get_or_create(queryset=owner.user_artists.all(),
                name=metadata.tags.artist[0], model=Artist, owner=owner)
    except:
        pass
    try:
        track.genre = get_or_create(queryset=owner.user_genres.all(),
                name=metadata.tags.genre[0], model=Genre, owner=owner)
    except:
        pass

    try:
        track.duration = timedelta(seconds=round(metadata.streaminfo.duration))
    except:
        pass

    # get track image

    return track

# note: to get abs path of track
# track.audio.path



# def reset_db(User)
#   delete current db 
#   for folder in user.userfolders
#       scan_folder(folder)
