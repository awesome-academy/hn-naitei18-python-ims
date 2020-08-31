
from django.urls import path, include

from . import views
from .views import *
from django.conf import settings


urlpatterns = [
	path('',index, name='index'),
	path('category/', CategoryListView.as_view(), name='category'),
	path('category/<int:pk>', CategoryDetailView.as_view(), name='category-detail'),
	path('song/', SongListView.as_view(), name='song'),
	path('song/<int:pk>', SongDetailView.as_view(), name='song-detail'),
	path('artist/', ArtistListView.as_view(), name='artist'),
	path('artist/<int:pk>', ArtistDetailView.as_view(), name='artist-detail'),
	path('profile', views.profile, name ='profile'),
    path('hotsong/', HotSongListView.as_view(), name='hot-song'),
	path('register/', register, name='register'),
	path('search-song/', SearchSongListView.as_view(), name='search'),
    path('station/', StationListView.as_view(), name='user-list'),
    path('station/<int:pk>', views.follow, name='follow'),
]
