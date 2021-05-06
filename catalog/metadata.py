from django.db.models import signals
from django.dispatch import receiver
from django.core.files.temp import NamedTemporaryFile

from catalog.models import Album, Artist, Genre, Track

from datetime import timedelta
import audio_metadata
import mimetypes
import os


@receiver(signals.post_delete, sender=Track)
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
    filename, ext = os.path.splitext(os.path.basename(file.name))
    track = Track(title=filename, owner=owner, audio=file)
    try:
        metadata = audio_metadata.load(file.temporary_file_path())
    except:
        if ext in ('.flac', '.mp3', '.aac', '.ogg', '.wav'): # .opus
            return track
        return None

    try:
        if metadata.tags.title[0]:
            track.title = metadata.tags.title[0]
    except:
        pass

    try:
        track.genre = get_or_create(queryset=owner.user_genres.all(),
                name=metadata.tags.genre[0], model=Genre, owner=owner)
    except:
        pass
    try:
        track.artist = get_or_create(queryset=owner.user_artists.all(),
                name=metadata.tags.artist[0], model=Artist, owner=owner)
    except:
        pass

    try:
        track.album = get_or_create(queryset=owner.user_albums.all(),
                name=metadata.tags.album[0], model=Album, owner=owner)
        if track.album.image == Album._meta.get_field('image').get_default():
            try:
                with NamedTemporaryFile(suffix=guess_extension(metadata.pictures[0].mime_type)) as temp:
                    temp.write(metadata.pictures[0].data)
                    track.album.image = temp
                    track.album.save()
            except:
                pass
        else:
            track.image = track.album.image

        # also need to get track_number and disc number
        # num, total = metadat.tags.discnumber[0].split('/') 
        # sometimes metadata will use discnumber and disctotal
        # num, total = metadata.tags.discnumber[0], metadata.tags.disctotal[0]
    except:
        pass

    try:
        track.duration = timedelta(seconds=round(metadata.streaminfo.duration))
    except:
        pass

    return track




# when looking through files will probably find a image maned cover or image 
# def reset_db(User)
#   delete current db 
#   for folder in user.userfolders
#       scan_folder(folder)
