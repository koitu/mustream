from rest_framework import serializers
from catalog.models import Artist, Album, Genre, Track, Playlist, UserProfile
from django.contrib.auth.models import User





class ListAlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ['id', 'name']
        read_only_fields = fields

class ListArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ['id', 'name']
        read_only_fields = fields

class ListGenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']
        read_only_fields = fields

class ListTrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = ['id', 'title']
        read_only_fields = fields


class AlbumSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(source='owner.username')
    album_tracks = ListTrackSerializer(many=True)

    class Meta:
        model = Album
        fields = ['id', 
                'name', 
                'owner', 
                'image',
                'album_tracks']
        read_only_fields = [x for x in fields if x != 'image']

class ArtistSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(source='owner.username')
    artist_tracks = ListTrackSerializer(many=True)

    class Meta:
        model = Artist
        fields = ['id', 
                'name', 
                'owner', 
                'image',
                'artist_tracks']
        read_only_fields = [x for x in fields if x != 'image']

class GenreSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(source='owner.username')
    genre_tracks = ListTrackSerializer(many=True)

    class Meta:
        model = Genre
        fields = ['id', 
                'name', 
                'owner', 
                'image',
                'genre_tracks']
        read_only_fields = [x for x in fields if x != 'image']




# TODO:

class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    adds `fields` argument that controls which fields should be displayed
    """
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)
        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


# used for the header with music controls
# class SimpleTrackSerializer(serializers.ModelSerializer):
#        fields = ['id', 
#                'title', 
#                'image',
#                'duration',
#                'album_track_number']


class TrackSerializer(DynamicFieldsModelSerializer):
    owner = serializers.CharField(source='owner.username')
    album = ListAlbumSerializer()
    artist = ListArtistSerializer()
    genre = ListGenreSerializer()

    class Meta:
        model = Track
        fields = ['id', 
                'title', 
                'owner', 
                'image',
#                'audio',
                'duration',
                'album_track_number',
                'album_disc_number',
                'album', 
                'artist', 
                'genre']
        read_only_fields = [x for x in fields if x != 'image']


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')

    class Meta:
        model = UserProfile
        fields = ['id',
                'username',
                'image',
                'shuffle',
                'current_track'
#                'saved_playlists'
                ]
        read_only_fields = ['id', 
                'username'
#                'saved_playlists'
                ]


class PlaylistSerializer(DynamicFieldsModelSerializer):
    owner = serializers.CharField(source='owner.username')

    class Meta:
        model = Playlist
        fields = ['id', 
                'name', 
                'owner', 
                'public']
        read_only_fields = ['id', 'owner']

class PlaylistTrackSerializer(DynamicFieldsModelSerializer):
    tracks = ListTrackSerializer(many=True)

    class Meta:
        model = Playlist
        fields = ['tracks']
