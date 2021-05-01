from catalog.models import Album, Artist, Genre, Track
from django.db import models
import audio-metadata


@receiver(models.signals.post_delete, sender=Track)
def delete_when_empty(sender, instance,  **kwargs):
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

    # probably want to delete image and audio off filesystem


# def reset_db(User)
#   delete current db ? # is it faster to compare diff and add/rm tracks/stuff or just wipe and genreate from files
#   for folder in user.userfolders
#       scan_folder(folder)

