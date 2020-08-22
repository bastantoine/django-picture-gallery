from django.urls import path

from .views import (
    HomeAdminView,
    AddAlbumView,
    ToggleProtectionAlbumView,
)

app_name = 'gallery_admin'

urlpatterns = [
    path('', HomeAdminView.as_view(), name='home'),
    path('album/add/', AddAlbumView.as_view(), name='add_album'),
    path('album/<int:id_album>/toggle-protection', ToggleProtectionAlbumView.as_view(), name='toggle_protection_album'),
]
