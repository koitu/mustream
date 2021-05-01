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
                'name', 
                'owner', 
                'image',
                'album_tracks']
        read_only_fields = ['id', 'name', 'owner', 'album_tracks']


class ArtistSerializer(DynamicFieldsModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Artist
        fields = ['id', 
                'name', 
                'owner', 
                'image',
                'artist_tracks']
        read_only_fields = ['id', 'name', 'owner', 'artist_tracks']


class GenreSerializer(DynamicFieldsModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Genre
        fields = ['id', 
                'name', 
                'owner', 
                'image',
                'genre_tracks']
        read_only_fields = ['id', 'name', 'owner', 'genre_tracks']


class TrackSerializer(DynamicFieldsModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Track
        fields = ['id', 
                'title', 
                'owner', 
                'image',
                'album', 
                'artist', 
                'genre']
        read_only_fields = ['id', 
                'title', 
                'owner', 
                'image', 
                'album', 
                'artist', 
                'genre']

    def create(self, validated_data):
        track = Track(
                title=validated_date['title'],
                image=validated_date['image']
                )
        track.save()
        return track


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



class PlaylistSerializer(DynamicFieldsModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Playlist
        fields = ['id', 
                'owner', 
                'public',
                'name', 
                'tracks']



class FolderSerializer(DynamicFieldsModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Folder
        fields = ['id', 
                'owner',
                'path']
