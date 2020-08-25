
from django.urls import path, include

from . import views
from .views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
	path('',index, name='index'),
	path('category/', CategoryListView.as_view(), name='category'),
	path('category/<int:pk>', CategoryDetailView.as_view(), name='category-detail'),
	path('song/', SongListView.as_view(), name='song'),
	path('song/<int:pk>', SongDetailView.as_view(), name='song-detail'),
	path('artist/', ArtistListView.as_view(), name='artist'),
	path('artist/<int:pk>', ArtistDetailView.as_view(), name='artist-detail'),
	path('profile',views.profile, name ='profile')
]
if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
