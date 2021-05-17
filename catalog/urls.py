from django.urls import path
from catalog import views

# we want the root to return the details of the person currently logged in
# other a sign in / sign up page

# should public be everyone looking to site or also logged in?
# add share to other user?


# should move users under admin
# add /accounts/profile/ (or change to redirect somewhere else)



# extend the user model (which app will store this this?) (how can this new model do the same things as the old one)
# create new app to actually play the media and updatedb (called control/management/run/player)

# if play album/artist/genre/user? with shuffle off then start with first song and play in alpha order
# otherwise choose a random song 
# is this done in js?

urlpatterns = [
    path('', views.APIRoot.as_view()),

    path('tracks/', 
        views.TrackList.as_view(),
        name='track-list'),
    path('tracks/<int:pk>/', views.TrackDetail.as_view()),
    path('tracks/<int:pk>/stream/', views.StreamTrack.as_view()),

    path('albums/', 
        views.AlbumList.as_view(),
        name='album-list'),
    path('albums/<int:pk>/', views.AlbumDetail.as_view()),

    path('artists/', 
        views.ArtistList.as_view(),
        name='artist-list'),
    path('artists/<int:pk>/', views.ArtistDetail.as_view()),

    path('genres/', 
        views.GenreList.as_view(),
        name='genre-list'),
    path('genres/<int:pk>/', views.GenreDetail.as_view()),

    path('playlists/', 
        views.PlaylistList.as_view(),
        name='playlist-list'),
    path('playlists/<int:pk>/', views.PlaylistDetail.as_view()),
    # and more for playlists
]
