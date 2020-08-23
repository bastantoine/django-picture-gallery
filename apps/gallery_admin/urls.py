from django.urls import path

from .views import (
    HomeAdminView,
    AddAlbumView,
    ToggleProtectionAlbumView,
    DeleteAlbumView,
    EditAlbumView,
    CreateUUIDView,
    DeleteUUIDView,
)

app_name = 'gallery_admin'

urlpatterns = [
    path('', HomeAdminView.as_view(), name='home'),
    path('album/add/', AddAlbumView.as_view(), name='add_album'),
    path('album/<int:id_album>/toggle-protection', ToggleProtectionAlbumView.as_view(), name='toggle_protection_album'),
    path('album/<int:id_album>/delete', DeleteAlbumView.as_view(), name='delete_album'),
    path('album/<int:id_album>/edit', EditAlbumView.as_view(), name='edit_album'),
    path('album/<int:id_album>/link/share', CreateUUIDView.as_view(), name='share_link_album'),
    path('album/<int:id_album>/link/delete', DeleteUUIDView.as_view(), name='delete_link_album'),
]
