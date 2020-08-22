from django.shortcuts import redirect, render
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
            'form': AlbumForm(),
        }
        return render(request, 'gallery_admin/add_album.html', context=context)

    def post(self, request):
        form = AlbumForm(request.POST)
        if form.is_valid():
            album = Album(**form.cleaned_data)
            album.save()
            return redirect('gallery_admin:home')
        context = {
            'form': form,
        }
        return render(request, 'gallery_admin/add_album.html', context=context)
