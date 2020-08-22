from django.urls import path

from .views import (
    HomeAdminView,
    AddAlbumView
)

app_name = 'gallery_admin'

urlpatterns = [
    path('', HomeAdminView.as_view(), name='home'),
    path('album/add/', AddAlbumView.as_view(), name='add_album'),
]
