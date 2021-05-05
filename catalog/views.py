from rest_framework.views import APIView
from rest_framework.reverse import reverse, reverse_lazy
from rest_framework.response import Response
from rest_framework import generics, mixins, permissions, status, parsers
from catalog.permissions import IsOwner, IsOwnerOrIsPublic
from django.http import Http404, HttpResponse
from django.core.exceptions import ValidationError

from django.core.files.uploadhandler import TemporaryFileUploadHandler
from django.contrib.auth.models import User
from catalog.models import Album, Artist, Genre, Track, Playlist, Folder
from catalog import serializers

from catalog.metadata import create_track_from_file
from rest_framework.parsers import MultiPartParser
import mimetypes
import os


# update permissions.py (might be broken right now)
# also make sure that permissions line up with expected behaviour


# api/
class APIRoot(APIView):
    def get(self, request):
        return Response({
            'tracks': reverse_lazy('track-list', request=request),
            'albums': reverse_lazy('album-list', request=request),
            'artists': reverse_lazy('artist-list', request=request),
            'genres': reverse_lazy('genre-list', request=request),
            #'playlists': reverse_lazy('playlist-list', request=request)
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



# TODO: add deletion by album/artist/genre 
# generics.RetrieveUpdateDestroyAPIView
# if this doesn't work properly might have to create ImageAlbumSerializer, api/albums/<pk>/update_cover

# api/albums/<pk>/ 
class AlbumDetail(generics.RetrieveUpdateAPIView):
       permission_classes = [IsOwner] # IsOwnerOrInPublicPlaylist
       queryset = Album.objects.all()
       serializer_class = serializers.AlbumSerializer

# api/artists/<pk>/
class ArtistDetail(generics.RetrieveUpdateAPIView):
       permission_classes = [IsOwner] # IsOwnerOrInPublicPlaylist
       queryset = Artist.objects.all()
       serializer_class = serializers.ArtistSerializer

# api/genres/<pk>/
class GenreDetail(generics.RetrieveUpdateAPIView):
       permission_classes = [IsOwner] # IsOwnerOrInPublicPlaylist
       queryset = Genre.objects.all()
       serializer_class = serializers.GenreSerializer



class TrackList(mixins.ListModelMixin, generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.ListTrackSerializer
    parser_classes = (MultiPartParser,) # limits what can be submitted?

    def get_queryset(self):
        return Track.objects.filter(owner=self.request.user)

    def initialize_request(self, request, *args, **kwargs):
        request.upload_handlers = [TemporaryFileUploadHandler(request)] 
        return super().initialize_request(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def put(self, request, format=None):
        try:
            # request.data['file'] seems to do the same thing
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
    permission_classes = [IsOwner] # IsOwnerOrInPublicPlaylist
    queryset = Track.objects.all()
    serializer_class = serializers.TrackSerializer


# playback of album/genre/playlist/tracks will be handled with js
# another option would be to return a url to a suitable next track based on playing album/artist/genre/playlist/all tracks and shuffle mode
# how to prevent repeating tracks when listening to album on shuffle
# another option would be a route that returns a random track from album/artist/genre/playlist/all tracks
# could load a rnadom subset of tracks in the user based on type of play that he user wants and another view will pop the tracks
# api/tracks/<pk>/stream
class StreamTrack(APIView):
    permission_classes = [IsOwner] # IsOwnerOrInPublicPlaylist

    def get(self, request, pk, *args, **kwargs):
        try:
            path = Track.objects.get(pk=pk).audio.path
            response = HttpResponse(open(path, 'rb'))
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


# /users/ 
# (admin only) list or create a new user
class UserList(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, format=None):
        users = User.object.all()
        serializer = Userserializer(users, many=True, fields=('id', 'username'))
        return Response(serializer.data)

    # what to do when user already exists? (how to update user?)
    def post(self, request, format=None):
        serializer = serializers.UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# /users/id/
# (admin and user only) get info/update/destroy a user
class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer



# TODO: will implement sharing via playlists
# /playlists/
# get: list playlists that the user owns
# put/post?: create a new empty playlist

# /playlists/id/
# get: list genres, albums, artists, and tracks added to playlist
# put/post/patch?: add genres, albums, artists, and tracks to playlist (by id) (only the ones that the user owns for now)

# /playlists/id/stream/
# play playlist (how to play song selected?)

# note that the genres, albums, artists, and tracks can be looked at by using the other api things

# class PlaylistList(generics.ListCreateAPIView):
#     permission_classes = [OtherPermissions]
#     queryset = Playlist.objects.all()
#     serializer_class = serializers.PlaylistSerializer
# 
#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)
# 
# 
# class PlaylistDetail(generics.RetrieveUpdateDestroyAPIView):
#     permission_classes = [OtherPermissions]
#     queryset = Playlist.objects.all()
#     serializer_class = serializers.PlaylistSerializer
