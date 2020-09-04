from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from apps.core.models import Album
from apps.lib.views import BaseView


class HomeView(BaseView):
    pagetitle = 'Home'

    def get(self, request):
        all_albums = Album.objects.filter(parent_album__exact=None)
        if not request.user.is_authenticated:
            # User not authenticated -> show only the non protected albums
            all_albums = all_albums.filter(is_protected=False)
        context = {
            'albums': all_albums,
        }
        return self.render(request, 'viewer/home.html', context=context)


class AlbumView(BaseView):

    def get(self, request, id_album=None, uuid=None):
        params = {'pk': id_album} if id_album else {'uuid__exact': uuid}
        album = get_object_or_404(Album, **params)
        if id_album and album.is_protected and not request.user.is_authenticated:
            # User is not authenticated and tried to access to the album using it's id -> do not permit access
            raise PermissionDenied
        self.pagetitle = album.name
        child_albums = Album.objects.filter(parent_album__exact=album)
        context = {
            'album': album,
            'child_albums': child_albums,
        }
        return self.render(request, 'viewer/album.html', context=context)
