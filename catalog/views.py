from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, mixins, permissions, status
from catalog.permissions import IsOwner, IsOwnerOrIsPublic
from django.http import Http404

from django.contrib.auth.models import User
from catalog.models import Album, Artist, Genre, Track, Playlist, Folder
from catalog.serializers import AlbumSerializer, ArtistSerializer, GenreSerializer, TrackSerializer, PlaylistSerializer, UserSerializer, FolderSerializer




# when updatedb only change album/genre/whatever when they are using the default image


# update permissions.py (might be broken right now)
# also make sure that permissions line up with expected behaviour


# api/
# give link to /tracks/ /ablums/ /genres/ /playlists/ /folders/




# api/albums/ 
class AlbumList(generics.ListAPIView):
       permission_classes = [permissions.IsAuthenticated]
       serializer_class = ListAlbumSerializer

       def get_queryset(self):
           return Album.objects.filter(owner=self.request.user)


# api/artists/ 
class ArtistList(generics.ListAPIView):
       permission_classes = [permissions.IsAuthenticated]
       serializer_class = ListArtistSerializer

       def get_queryset(self):
           return Artist.objects.filter(owner=self.request.user)


# api/genres/ 
class GenreList(generics.ListAPIView):
       permission_classes = [permissions.IsAuthenticated]
       serializer_class = ListGenreSerializer

       def get_queryset(self):
           return Genre.objects.filter(owner=self.request.user)



# TODO: add deletion by album/artist/genre 
# generics.RetrieveUpdateDestroyAPIView
# if this does work properly might have to create ImageAlbumSerializer, api/albums/<pk>/update



# api/albums/<pk>/ 
class AlbumDetail(generics.RetrieveUpdateAPIView):
       permission_classes = [IsOwner] # IsOwnerOrInPublicPlaylist
       queryset = Album.objects.all()
       serializer_class = AlbumSerializer

# api/artists/<pk>/
class ArtistDetail(generics.RetrieveUpdateAPIView):
       permission_classes = [IsOwner] # IsOwnerOrInPublicPlaylist
       queryset = Artist.objects.all()
       serializer_class = ArtistSerializer

# api/genres/<pk>/
class GenreDetail(generics.RetrieveUpdateAPIView):
       permission_classes = [IsOwner] # IsOwnerOrInPublicPlaylist
       queryset = Genre.objects.all()
       serializer_class = GenreSerializer

    






class TrackList(mixins.ListModelMixin, generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ListTrackSerializer

    def get_queryset(self):
       return Track.objects.filter(owner=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, format=None):
        tracks = []
        for file in request.FILES.getlist('file'):
            try:
                tracks.append(create_track_from_file(file, request.user))
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST) # double check correct response
        for track in tracks:
            if track and track.is_valid():
                track.save()
        return Response(status=status.HTTP_201_CREATED)) 

    # return Response(status=status.HTTP_400_BAD_REQUEST) # also return errors
    # track.data track.errors

    # response should return uploads and possible errors

    def put(self, request, format=None):
        return self.post(request, format=format)


# get, delete api/tracks/<pk>/
class TrackDetail(generics.RetrieveDestroyAPIView):
    permission_classes = [IsOwner] # IsOwnerOrInPublicPlaylist
    queryset = Track.objects.all()
    serializer_class = TrackSerializer





#   # route: api/track/<track_id>/stream
#   class TrackStreamRoute(APIView):
#       permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#   
#       def get(self, request, *args, **kwargs):
#           try:
#               track = Track.objects.get(id=kwargs['track_id'])
#               fsock = track.audio_src.open('rb')
#               response = HttpResponse(fsock)
#               response['Content-Type'] = track.audio_format
#               response['Content-Disposition'] = 'attachment; filename=%s' % (track.file_name.replace(' ', '-'),)
#               response['Content-Length'] = os.path.getsize(track.audio_src.path)
#               response['Accept-Ranges'] = 'bytes'
#               return response
#           except Track.DoesNotExist:
#               raise Http404
#           except Exception as e:
#               print(e)
#           return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# /tracks/stream/
# /tracks/id/stream/
# play tracks under /tracks/ depending on shuffle



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
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# /users/id/
# (admin and user only) get info/update/destroy a user
class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserSerializer



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
#     serializer_class = PlaylistSerializer
# 
#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)
# 
# 
# class PlaylistDetail(generics.RetrieveUpdateDestroyAPIView):
#     permission_classes = [OtherPermissions]
#     queryset = Playlist.objects.all()
#     serializer_class = PlaylistSerializer
