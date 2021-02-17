from rest_framework import serializers
from mustream.core.models import Track, Album, Artist, Genre, Collection, MuUser, Playlist
from django.contrib.auth.models import User



class MuUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MuUser
        fields = ['profile_picture']


class UserSerializer(serializers.ModelSerializer):
    profile_picture = MuUserSerializer(many=False, read_only=False)
    collection = serializers.PrimaryKeyRelatedField(many=False, queryset=Collection.objects.all())
    playlists = serializers.PrimaryKeyRelatedField(many=True, queryset=Playlist.objects.all())

    classMeta:
        model = User
        fields = ['id', 'username', 'profile_picture', 'collection', 'playlists']


class CollectionSerializer(serializers.ModelSerializer):
    editors = MuUserSerializer(many=True)
    viewers = MuUserSerializer(many=True)

    class Meta:
        model = Collection
        fields = ['public']

class PlaylistSerializer(serializers.ModelSerializer):
    editors = MuUserSerializer(Many=True)
    viewers = MuUserSerializer(Many=True)

    class Meta:
        model = Playlist
        fields = ['name', 'image', 'date_created', 'date_modified', 'public']


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ['name', 'image', 'comments']

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['name']

class AlbumSerializer(serializers.ModelSerializer):
    artist = ArtistSerializer(many=True)
    
    class Meta:
        model = Album
        fields = ['name', 'image', 'discs', 'tracks']

class TrackSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    album = AlbumSerializer()
    artist = ArtistSerializer(many=True)
    genres = GenreSerializer(many=True)

    class Meta:
        model = Track
        fields = ['owner',
                'title', 
                'location', 
                'image', 
                'length', 
                'release_date', 
                'disc_number', 
                'track_number']
