from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.views import View

from .models import Album, Picture


class HomeView(View):

    def get(self, request):
        all_albums = Album.objects.all()
        if not request.user.is_authenticated:
            # User not authenticated -> show only the non protected albums
            all_albums = all_albums.filter(is_protected=False)
        context = {
            'albums': all_albums,
        }
        return render(request, 'viewer/home.html', context=context)


class AlbumView(View):

    def get(self, request, id_album):
        album = get_object_or_404(Album, pk=id_album)
        if album.is_protected and not request.user.is_authenticated:
            # User is not authenticated -> do not permit access
            raise PermissionDenied
        context = {
            'album': album,
        }
        return render(request, 'viewer/album.html', context=context)
