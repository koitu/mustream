from catalog.models import Album, Artist, Genre, Track, Playlist, Folder
from django.contrib.auth.models import User
from catalog.serializers import AlbumSerializer, ArtistSerializer, GenreSerializer, TrackSerializer, PlaylistSerializer, UserSerializer, FolderSerializer
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from catalog.permissions import TrackPermissions, OtherPermissions, IsOwner



# update so that on save will update album + genre + artist that the track belongs to 

# when updatedb only change album/genre/whatever when they are using the default image
    

# /tracks/
# return all tracks that belong to a person or create a new one
class TrackList(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        tracks = Track.objects.filter(owner=request.user)
        serializer = TrackSerializer(tracks, many=True, fields=('id', 'title'))
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = TrackSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# /tracks/id/
# get info or destory a track
class TrackDetail(generics.RetrieveDestroyAPIView):
    permission_classes = [IsOwner]
    queryset = Track.objects.all()
    serializer_class = TrackSerializer

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


# /
# give link to /tracks/ /ablums/ /genres/ /playlists/ /folders/


class AlbumArtistGenreList(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, Model, Serializer, format=None):
        objects = Model.object.filter(owner=request.user)
        serializer = Serializer(objects, many=True, fields=('id', 'name'))
        return Response(serializer.data)

# /albums/
class AlbumList(AlbumArtistGenreList):
        super().get(request, Album, AlbumSerializer, format=format)

# /artists/
class ArtistList(AlbumArtistGenreList):
    def get(self, request, format=None):
        super().get(request, Artist, ArtistSerializer, format=format)

# /genres/
class GenreList(AlbumArtistGenreList):
    def get(self, request, format=None):
        super().get(request, Genre, GenreSerializer, format=format)




def get_object(pk, Model):
    try:
        return Model.objects.get(pk=pk)
    except Model.DoesNotExist:
        raise Http404


class AlbumArtistGenreDetail(APIView):
    permission_classes = [IsOwnerOrPublic]

    def get(self, request, pk, Model, ModelSerializer, format=None):
        objects = self.get_object(pk, Model)
        serializer = ModelSerializer(objects)
        return Response(serializer.data)

    def patch(self, request, pk, Model, ModelSerializer, format=None):
        a_object = self.get_object(pk, Model)
        serializer = ModelSerializer(album, data=request.data, partial=True)
        a_object.cover = serializer.cover
        if a_object.is_valid():
            a_object.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# /albums/id/
class AblumDetail(AlbumArtistGenreDetail):
    def get(self, request, pk, format=None):
        super().get(request, pk, Album, AlbumSerializer, format=format)

    def patch(self, request, pk, format=None):
        super().patch(request, pk, Album, AlbumSerializer, format=format)

# /artists/id/
class ArtistDetail(AlbumArtistGenreDetail):
    def get(self, request, pk, format=None):
        super().get(request, pk, Artist, ArtistSerializer, format=format)

    def patch(self, request, pk, format=None):
        super().patch(request, pk, Artist, ArtistSerializer, format=format)

# /genres/id/
class GenreDetail(AlbumArtistGenreDetail):
    def get(self, request, pk, format=None):
        super().get(request, pk, Genre, GenreSerializer, format=format)

    def patch(self, request, pk, format=None):
        super().patch(request, pk, Genre, GenreSerializer, format=format)





# will implement sharing via playlists later
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







# # /albums/
# class TrackList(APIView):
#     permission_classes = [permissions.IsAuthenticated]
# 
#     def get(self, request, format=None):
#         tracks = Track.objects.filter(owner=request.user)
#         serializer = TrackSerializer(tracks, many=True, fields=('id', 'name'))
#         return Response(serializer.data)
# 
# 
# # /ablums/id/
# class AlbumDetail(APIView):
#     permission_classes = [IsOwner]
# 
#     def get_album(self, pk):
#         try:
#             return Album.objects.get(pk=pk)
#         except Album.DoesNotExist:
#             raise Http404
# 
#     def get(self, request, pk, format=None):
#         album = self.get_album(pk)
#         serializer = AlbumSerializer(album)
#         return Response(serializer.data)
# 
#     def patch(self, request, pk, format=None):
#         album = self.get_album(pk)
#         serializer = AlbumSerializer(album, data=request.data, partial=True)
#         album.cover = serializer.cover
#         if album.is_valid():
#             album.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





