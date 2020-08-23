from django.urls import path

from .views import (
    HomeAdminView,
    AddAlbumView,
    ToggleProtectionAlbumView,
    DeleteAlbumView,
    EditAlbumView,
)

app_name = 'gallery_admin'

urlpatterns = [
    path('', HomeAdminView.as_view(), name='home'),
    path('album/add/', AddAlbumView.as_view(), name='add_album'),
    path('album/<int:id_album>/toggle-protection', ToggleProtectionAlbumView.as_view(), name='toggle_protection_album'),
    path('album/<int:id_album>/delete', DeleteAlbumView.as_view(), name='delete_album'),
    path('album/<int:id_album>/edit', EditAlbumView.as_view(), name='edit_album'),
]
