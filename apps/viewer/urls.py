from django.urls import path

from .views import (
    HomeView,
    AlbumView
)

app_name = 'viewer'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('album/<int:id_album>', AlbumView.as_view(), name='album_id'),
    path('album/<uuid:uuid>', AlbumView.as_view(), name='album_uuid'),
]
