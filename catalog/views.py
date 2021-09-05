from rest_framework import generics, mixins, permissions, status
from rest_framework.views import APIView
from rest_framework.reverse import reverse
from rest_framework.response import Response

from django.http import Http404, HttpResponse
from django.core.exceptions import ValidationError
# from django.contrib.auth.models import User
from django.core.files.uploadhandler import TemporaryFileUploadHandler

from catalog import serializers
from catalog.models import Album, Artist, Genre, Track, Playlist
from catalog.metadata import create_track_from_file
from catalog.permissions import IsOwner, IsOwnerOrIsPublic

import mimetypes
import os


# api/
class APIRoot(APIView):
    def get(self, request):
        return Response({
            'tracks': reverse('track-list', request=request),
            'albums': reverse('album-list', request=request),
            'artists': reverse('artist-list', request=request),
            'genres': reverse('genre-list', request=request),
            'playlists': reverse('playlist-list', request=request)
        })


# api/albums/ 
class AlbumList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.ListAlbumSerializer

    def get_queryset(self):
        return Album.objects.filter(owner=self.request.user)


# api/artists/ 
class ArtistList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.ListArtistSerializer

    def get_queryset(self):
        return Artist.objects.filter(owner=self.request.user)


# api/genres/ 
class GenreList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.ListGenreSerializer

    def get_queryset(self):
        return Genre.objects.filter(owner=self.request.user)


# api/albums/<pk>/ 
class AlbumDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwner]
    queryset = Album.objects.all()
    serializer_class = serializers.AlbumSerializer


# api/artists/<pk>/
class ArtistDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwner]
    queryset = Artist.objects.all()
    serializer_class = serializers.ArtistSerializer


# api/genres/<pk>/
class GenreDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwner]
    queryset = Genre.objects.all()
    serializer_class = serializers.GenreSerializer


class TrackList(mixins.ListModelMixin, generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.ListTrackSerializer

    def get_queryset(self):
        return Track.objects.filter(owner=self.request.user)

    def initialize_request(self, request, *args, **kwargs):
        request.upload_handlers = [TemporaryFileUploadHandler(request)]
        return super().initialize_request(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def put(self, request, format=None):
        try:
            if request.FILES['file'].size > 2e8:
                return Response(status=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE)
            track = create_track_from_file(request.FILES['file'], request.user)
            if track:
                track.validate_unique()
                track.save()
                return Response(status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            print(e)
            return Response(status=status.HTTP_409_CONFLICT)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, format=None):
        return self.put(request, format=format)


# api/tracks/<pk>/
class TrackDetail(generics.RetrieveDestroyAPIView):
    permission_classes = [IsOwner]
    queryset = Track.objects.all()
    serializer_class = serializers.TrackSerializer


# api/tracks/<pk>/stream/
class StreamTrack(APIView):
    permission_classes = [IsOwner]

    def get(self, request, pk, *args, **kwargs):
        try:
            path = Track.objects.get(pk=pk).audio.path
            with open(path, 'rb') as file:
                response = HttpResponse(file)
            response['Content-Type'] = mimetypes.guess_type(path)[0]
            response['Content-Disposition'] = "attachment; filename=%s" % (os.path.basename(path).replace(' ', '-'))
            response['Content-Length'] = os.path.getsize(path)
            response['Accept-Ranges'] = 'bytes'
            return response
        except Track.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# api/playlists/
class PlaylistList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.PlaylistSerializer

    def get_queryset(self):
        return Playlist.objects.filter(owner=self.request.user)


# api/playlists/<pk>/
class PlaylistDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrIsPublic]
    queryset = Playlist.objects.all()
    serializer_class = serializers.PlaylistSerializer


# api/playlists/<pk>/tracks/
class PlaylistDetail(generics.ListAPIView):
    permission_class = [IsOwnerOrIsPublic]
    queryset = Playlist.objects.all()
    serializer_class = serializers.PlaylistTrackSerializer


# api/playlists/<pk_pk>/tracks/<pk>/
class PlaylistTrack(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_playlist(self, pk):
        try:
            return Playlist.objects.get(pk=pk)
        except Playlist.DoesNotExist:
            raise Http404

    def get_track(self, pk):
        try:
            return Track.objects.get(pk=pk)
        except Track.DoesNotExist:
            raise Http404

    def get(self, request, pk, list_pk, *args, **kwargs):
        playlist = self.get_playlist(pk=list_pk)
        if playlist.public or playlist.owner == request.user:
            try:
                serializer = serializers.TrackSerializer(playlist.tracks.get(pk=pk))
                return Response(serializer.data)
            except:
                raise Http404
        return Response(status=status.HTTP_403_FORBIDDEN)

    def post(self, request, pk, list_pk, *args, **kwargs):
        playlist = self.get_playlist(pk=list_pk)
        if playlist.owner == request.user:
            track = self.get_track(pk=pk)
            if track.owner == request.user:
                playlist.tracks.add(track)
        return Response(status=status.HTTP_403_FORBIDDEN)

    def put(self, request, pk, list_pk, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def delete(self, request, pk, list_pk, *args, **kwargs):
        playlist = self.get_playlist(pk=list_pk)
        if playlist.owner == request.user:
            track = self.get_track(pk=pk)
            if track.owner == request.user:
                playlist.tracks.remove(track)
        return Response(status=status.HTTP_403_FORBIDDEN)


# api/playlists/<pk_pk>/tracks/<pk>/stream/
class StreamPlaylistTrack(StreamTrack):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk, list_pk, *args, **kwargs):
        try:
            playlist = Playlist.objects.get(pk=list_pk)
        except Playlist.DoesNotExist:
            raise Http404
        if playlist.public or playlist.owner == request.user:
            return super().get(request, pk, *args, **kwargs)
        return Response(status=status.HTTP_403_FORBIDDEN)
