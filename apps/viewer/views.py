from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.views import View

from apps.core.models import Album, Picture


class HomeView(View):

    def get(self, request):
        all_albums = Album.objects.filter(parent_album__exact=None)
        if not request.user.is_authenticated:
            # User not authenticated -> show only the non protected albums
            all_albums = all_albums.filter(is_protected=False)
        context = {
            'albums': all_albums,
        }
        return render(request, 'viewer/home.html', context=context)


class AlbumView(View):

    def get(self, request, id_album=None, uuid=None):
        params = {'pk': id_album} if id_album else {'uuid__exact': uuid}
        album = get_object_or_404(Album, **params)
        if id_album and album.is_protected and not request.user.is_authenticated:
            # User is not authenticated and tried to access to the album using it's id -> do not permit access
            raise PermissionDenied
        child_albums = Album.objects.filter(parent_album__exact=album)
        context = {
            'album': album,
            'child_albums': child_albums,
        }
        return render(request, 'viewer/album.html', context=context)
