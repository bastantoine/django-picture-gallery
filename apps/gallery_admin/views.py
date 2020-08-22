from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from apps.core.models import Album

from .forms import AlbumForm


class HomeAdminView(View):

    def get(self, request):
        context = {
            'albums': Album.objects.all(),
        }
        return render(request, 'gallery_admin/home.html', context=context)


class AddAlbumView(View):

    def get(self, request):
        context = {
            'form': AlbumForm('gallery_admin:add_album', 'Create album', ),
        }
        return render(request, 'gallery_admin/add_album.html', context=context)

    def post(self, request):
        form = AlbumForm('gallery_admin:add_album', 'Create album', request.POST)
        if form.is_valid():
            album = Album(**form.cleaned_data)
            album.save()
            return redirect('gallery_admin:home')
        context = {
            'form': form,
        }
        return render(request, 'gallery_admin/add_album.html', context=context)


class ToggleProtectionAlbumView(View):

    def get(self, request, id_album):
        album = get_object_or_404(Album, pk=id_album)
        album.is_protected = not album.is_protected
        album.save()
        return redirect('gallery_admin:home')


class DeleteAlbumView(View):

    def get(self, request, id_album):
        album = get_object_or_404(Album, pk=id_album)
        album.delete()
        return redirect('gallery_admin:home')
