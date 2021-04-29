from django.urls import path
from . import views

# we want the root to return the details of the person currently logged in
# other a sign in / sign up page

# should public be everyone looking to site or also logged in?
# add share to other user?


# should move users under admin


# extend the user model (which app will store this this?) (how can this new model do the same things as the old one)
# create new app to actually play the media and updatedb (called control/management/run/player)

# if play album/artist/genre/user? with shuffle off then start with first song and play in alpha order
# otherwise choose a random song 
# is this done in js?

urlpatterns = [
    path('tracks/', views.TrackList.as_view()),
    path('tracks/<int:pk>/', views.TrackDetail.as_view()),

    path('albums/', views.AlbumList.as_view()),
    path('albums/<int:pk>/', views.AlbumDetail.as_view()),

    path('artists/', views.ArtistList.as_view()),
    path('artists/<int:pk>/', views.ArtistDetail.as_view()),

    path('genres/', views.GenreList.as_view()),
    path('genres/<int:pk>/', views.GenreDetail.as_view()),

    path('playlists/', views.PlaylistList.as_view()),
    path('playlists/<int:pk>/', views.PlaylistDetail.as_view()),

    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
]
