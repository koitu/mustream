from rest_framework import serializers
from mustream.core.models import Track, Album, Artist, Genre, Collection, Profile, Playlist
from django.contrib.auth.models import User



class UserSerializer(serializers.ModelSerializer):
    profile_picture = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'profile_picture']


class PlaylistSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    #editors = UserSerializer(Many=True)
    #viewers = UserSerializer(Many=True)

    class Meta:
        model = Playlist
        fields = ['owner', 'name', 'image', 'date_created', 'date_modified', 'public']


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
        fields = ['name', 'artist', 'image', 'discs', 'tracks']

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
