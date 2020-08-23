from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View

from apps.core.models import Album, Picture

from .forms import AlbumForm, PictureForm


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
        return render(request, 'gallery_admin/form.html', context=context)

    def post(self, request):
        form = AlbumForm('gallery_admin:add_album', 'Create album', request.POST)
        if form.is_valid():
            album = Album(**form.cleaned_data)
            album.save()
            return redirect('gallery_admin:home')
        context = {
            'form': form,
        }
        return render(request, 'gallery_admin/form.html', context=context)


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


class EditAlbumView(View):

    def get(self, request, id_album):
        album = get_object_or_404(Album, pk=id_album)
        context = {
            'form': AlbumForm(
                reverse('gallery_admin:edit_album', kwargs={'id_album':id_album}),
                'Update album',
                instance=album,
            ),
        }
        return render(request, 'gallery_admin/form.html', context=context)

    def post(self, request, id_album):
        album = get_object_or_404(Album, pk=id_album)
        form = AlbumForm(
            reverse('gallery_admin:edit_album', kwargs={'id_album':id_album}),
            'Update album',
            data=request.POST,
        )
        if form.is_valid():
            album.update(**form.cleaned_data)
            return redirect('gallery_admin:home')
        context = {
            'form': form,
        }
        return render(request, 'gallery_admin/form.html', context=context)


class CreateUUIDView(View):

    def get(self, request, id_album):
        album = get_object_or_404(Album, pk=id_album)
        album.add_uuid()
        link = '{scheme}://{host}{path}'.format(
            scheme=request.scheme,
            host=request.get_host(),
            path=reverse('viewer:album_uuid', kwargs={'uuid': album.uuid})
        )
        context = {
            'link': link,
        }
        return render(request, 'gallery_admin/create_uuid.html', context=context)


class DeleteUUIDView(View):

    def get(self, request, id_album):
        album = get_object_or_404(Album, pk=id_album)
        album.update(uuid=None)
        return redirect('gallery_admin:home')


class AddPictureView(View):

    def get(self, request, id_album=None):
        instance=None
        if id_album:
            album = get_object_or_404(Album, pk=id_album)
            instance = Picture(album=album)
        context = {
            'form': PictureForm('gallery_admin:add_picture', 'Add picture', instance=instance),
        }
        return render(request, 'gallery_admin/form.html', context=context)
