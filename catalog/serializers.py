from rest_framework import serializers
from catalog.models import Artist, Album, Genre, Track, Playlist

class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ['name', 'album_tracks']


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ['name', 'artist_tracks']


class GenreSerializer(serializers.GenreSerializer):
    class Meta:
        model = ['genre', 'genre_tracks']


class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = ['title', 'album', 'artist', 'genre']


class PlaylistSerializer(serializers.ModelSerializer):
    playlist_tracks = PrimaryKeyRelatedField(read_only=True, many=True) # unsure about this

    class Meta:
        model = Playlist
        fields = ['name', 'playlist_tracks']

