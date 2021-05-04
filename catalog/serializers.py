from rest_framework import serializers
from catalog.models import Artist, Album, Genre, Track, Playlist, Folder
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



# if id is set on model/database level we might not need it for some serializers



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


# extend this and use in the later parts
class UserSerializer(DynamicFieldsModelSerializer):
    user_tracks = ListTrackSerializer(many=True)
    user_albums = ListAlbumSerializer(many=True)
    user_artists = ListArtistSerializer(many=True)
    user_genres = ListGenreSerializer(many=True)

    class Meta:
        model = User
        fields = ['id', 
                'username', 
                'user_tracks', 
                'user_artists',
                'user_albums', 
                'user_genres']
        read_only_fields = fields # might want to change later



# TODO:

class PlaylistSerializer(DynamicFieldsModelSerializer):
    owner = serializers.CharField(source='owner.username')

    class Meta:
        model = Playlist
        fields = ['id', 
                'owner', 
                'public',
                'name', 
                'tracks']



class FolderSerializer(DynamicFieldsModelSerializer):
    owner = serializers.CharField(source='owner.username')

    class Meta:
        model = Folder
        fields = ['id', 
                'owner',
                'path']
