from rest_framework import serializers
from catalog.models import Artist, Album, Genre, Track, Playlist
from django.contrib.auth.models import User

# remember to either set read_only=True or queryst=<something>
# might need for playlistserializer (but my default I'm pretty sure they pull the pk of the objects attached
#    tracks = serializers.PrimaryKeyRelatedField(queryset=Track.objects.all(), many=True)

class AlbumSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Album
        fields = ['id', 
                'owner', 
                'pubilc',
                'name', 
                'album_tracks']


class ArtistSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Artist
        fields = ['id', 
                'owner', 
                'public',
                'name', 
                'artist_tracks']


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = ['id', 
                'name', 
                'genre_tracks']


class TrackSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    # get the username of the owner

    class Meta:
        model = Track
        fields = ['id', 
                'owner', 
                'public',
                'force_private',
                'title', 
                'album', 
                'artist', 
                'genre']


class PlaylistSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Playlist
        fields = ['id', 
                'owner', 
                'public',
                'name', 
                'tracks']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 
                'username', 
                'user_tracks', 
                'user_playlists', 
                'user_albums', 
                'user_artists']
