from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View

from apps.core.models import Album, Picture

from .forms import AlbumForm, PictureForm, LoginForm


class BaseProtectedView(View):

    def dispatch(self, request, *args, **kwargs):
        if not (request.user and request.user.is_authenticated):
            return redirect('%s?next=%s' % (reverse('gallery_admin:login'), request.path))
        return super(BaseProtectedView, self).dispatch(request, *args, **kwargs)


class HomeAdminView(BaseProtectedView):

    def get(self, request):
        context = {
            'albums': Album.objects.all(),
        }
        return render(request, 'gallery_admin/home.html', context=context)


class AddAlbumView(BaseProtectedView):

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


class ToggleProtectionAlbumView(BaseProtectedView):

    def get(self, request, id_album):
        album = get_object_or_404(Album, pk=id_album)
        album.is_protected = not album.is_protected
        album.save()
        return redirect('gallery_admin:home')


class DeleteAlbumView(BaseProtectedView):

    def get(self, request, id_album):
        album = get_object_or_404(Album, pk=id_album)
        album.delete()
        return redirect('gallery_admin:home')


class EditAlbumView(BaseProtectedView):

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


class CreateUUIDView(BaseProtectedView):

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


class DeleteUUIDView(BaseProtectedView):

    def get(self, request, id_album):
        album = get_object_or_404(Album, pk=id_album)
        album.update(uuid=None)
        return redirect('gallery_admin:home')


class AddPictureView(BaseProtectedView):

    def get(self, request, id_album=None):
        instance=None
        if id_album:
            album = get_object_or_404(Album, pk=id_album)
            instance = Picture(album=album)
        context = {
            'form': PictureForm('gallery_admin:add_picture', 'Add picture', instance=instance),
        }
        return render(request, 'gallery_admin/form.html', context=context)

    def post(self, request, id_album=None):
        form = PictureForm('gallery_admin:add_picture', 'Add picture', data=request.POST, files=request.FILES)
        if form.is_valid():
            for file in request.FILES.getlist('path'):
                picture = Picture(album=form.cleaned_data['album'], path=file)
                picture.save()
            return redirect('gallery_admin:home')
        context = {
            'form': form,
        }
        return render(request, 'gallery_admin/form.html', context=context)


class LoginView(View):

    def get(self, request):
        context = {
            'form': LoginForm('gallery_admin:login', 'Login')
        }
        return render(request, 'gallery_admin/form.html', context=context)

    def post(self, request):
        form = LoginForm('gallery_admin:login', 'Login', data=request.POST)
        if form.is_valid():
            user = authenticate(request, **form.cleaned_data)
            if user:
                login(request, user)
                if request.GET.get('next'):
                    return redirect(request.GET.get('next'))
                return redirect('gallery_admin:home')
        context = {
            'form': form,
        }
        return render(request, 'gallery_admin/form.html', context=context)


class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect('viewer:home')
