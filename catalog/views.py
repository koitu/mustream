from catalog.models import Album, Artist, Genre, Track, Playlist
from django.contrib.auth.models import User
from catalog.serializers import AlbumSerializer, ArtistSerializer, GenreSerializer, TrackSerializer, PlaylistSerializer, UserSerializer
from rest_framework import generics, permissions
from catalog.permissions import TrackPermissions, OtherPermissions

class TrackList(generics.ListCreateAPIView):
    permission_classes = [TrackPermissions]
    queryset = Track.objects.all()
    serializer_class = TrackSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TrackDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [TrackPermissions]
    queryset = Track.objects.all()
    serializer_class = TrackSerializer



class AlbumList(generics.ListCreateAPIView):
    permission_classes = [OtherPermissions]
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class AlbumDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [OtherPermissions]
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer



class ArtistList(generics.ListCreateAPIView):
    permission_classes = [OtherPermissions]
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ArtistDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [OtherPermissions]
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer



class GenreList(generics.ListCreateAPIView):
    permission_classes = [OtherPermissions]
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class GenreDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [OtherPermissions]
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer



class PlaylistList(generics.ListCreateAPIView):
    permission_classes = [OtherPermissions]
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PlaylistDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [OtherPermissions]
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer



class UserList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer
