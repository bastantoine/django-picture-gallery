from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.views import View

from .models import Album, Picture


class HomeView(View):

    def get(self, request):
        context = {
            'albums': Album.objects.all(),
        }
        return render(request, 'viewer/home.html', context=context)


class AlbumView(View):

    def get(self, request, id_album):
        album = get_object_or_404(Album, pk=id_album)
        context = {
            'album': album,
        }
        return render(request, 'viewer/album.html', context=context)
