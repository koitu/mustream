"""mustream URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from mustream.core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),

    path('api/users/', views.UserList.as_view()),
    path('api/users/<int:pk>/', views.UserDetail.as_view()),

    path('api/tracks/', views.TrackList.as_view()),
    path('api/tracks/<int:pk>/', views.TrackDetail.as_view()),

#    path('api/playlists/', views.PlaylistList.as_view()),
#    path('api/playlists/<int:pk>/', views.PlaylistDetail.as_view()),
#
#    path('api/albums/', views.AlbumList.as_view()),
#    path('api/albums/<int:pk>/', views.AlbumDetail.as_view()),
#
#    path('api/genres/', views.GenreList.as_view()),
#    path('api/genres/<int:pk>/', views.GenreDetail.as_view()),
]
