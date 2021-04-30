from rest_framework import serializers
from catalog.models import Artist, Album, Genre, Track, Playlist, Folder
from django.contrib.auth.models import User



# add to Meta:  read_only_fields = ['id', 'owner']




class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)

        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class AlbumSerializer(DynamicFieldsModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Album
        fields = ['id', 
                'owner', 
                'name', 
                'album_tracks']


class ArtistSerializer(DynamicFieldsModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Artist
        fields = ['id', 
                'owner', 
                'name', 
                'artist_tracks']


class GenreSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = ['id', 
                'name', 
                'genre_tracks']


class TrackSerializer(DynamicFieldsModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Track
        fields = ['id', 
                'owner', 
                'title', 
                'album', 
                'artist', 
                'genre']


class PlaylistSerializer(DynamicFieldsModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Playlist
        fields = ['id', 
                'owner', 
                'public',
                'name', 
                'tracks']


class UserSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = User
        fields = ['id', 
                'username', 
                'user_tracks', 
                'user_playlists', 
                'user_folders', 
                'user_albums', 
                'user_artists']

class FolderSerializer(DynamicFieldsModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Folder
        fields = ['id', 
                'owner',
                'path']
