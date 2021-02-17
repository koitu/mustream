from mustream.core.models import MuUser, Collection, Artist, Playlist, Album, Genre, Track
from mustream.core.serializers import MuUserSerializer, CollectionSerializer, ArtistSerializer, PlaylistSerializer, AlbumSerializer, GenreSerializer, TrackSerializer, UserSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework import permissions
from mustream.core.permissions import IsOwnerOrReadOnly

from django.contrib.auth.models import User


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class TrackList(generics.ListCreateAPIView):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
            IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    # get post (list all or create new)

class TrackDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
            IsOwnerOrReadOnly]
    # get put, delete (retieve, update, or delete)

#class MuUserDetails(generics.RetrieveUpdateDestroyAPIView):
    # get put delete
#    queryset = MuUser.objects.all()
#    serializer_class = MuUserSerializer

# class MuUserList(generics.ListCreateAPIView):
# get post

#class MuUser(APIView):
#
#    def get_user(self, username):
#        try:
#            return MuUser.objects.get(username=username)
#        except MuUser.DoesNotExist:
#            raise Http404
#        # where does auth occur?
#
#    def get(self, request, username, format=None):
#        muuser = self.get_user(username)
#        serializer = MuUserSerializer(muuser)
#        return Response(serializer.data)
#
#    def put(self, request, username, format=None):
#        muuser = self.get_user(username)
#        serializer = MuUserSerializer(muuser, data=request.data) # what is request.data?
#        # needs varfy for premissions and existence
#        if serializer.is_valid():
#            serializer.save()
#            return Response(serializer.data)
#        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#    def delete(self, request, username, format=None):
#        muuser = self.get_object(username)
#        muuser.delete()
#        return Response(status=status.HTTP_204_NO_CONTENT)



# log to history if track was listened to for x seconds

# sort by date, alpha or other

# front page (like spotify)
# history of tracks played
# recently played albums
# recently added albums
# search menu

# bottom/top bar (hide when no track?) (like nextcloud/spotify)
# controls to go forward/back tracks + play/pause (put stop somewhere)
# current track art + name + artist (if clicked will try to bring to location on tab of song)
# time through current track
# volume (inc only by 5%)
# shuffle
# loop

# sidebar (like nextcloud)
# Userpage, Collection, Albums + Artists, Genres (folders?) <sep> all playlists with add playlist at bot
# info sidebar
# file path
# general info
# technical info

# Userpage (like myanimelist profile)
# short discription of person
# favorate songs 
# favorate albums
# favorate playlists
# favorate artists
# folders to look at
# upload more music 

# Collection (like nextcloud all tracks tab)
# list of all tracks by <artist> - <track>
# id number and quick move by alphabet

# Albums + Artists (nextcloud)
# sort alpha/whatever order for artists
# all albums by artist under
# what to do if album has multple artists???

# Genres
# shortened list of tracks 
# Large list of unknown genre tracks
