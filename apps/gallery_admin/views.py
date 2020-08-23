from django.shortcuts import render
from django.views import View

from apps.core.models import Album


class HomeAdminView(View):

    def get(self, request):
        context = {
            'albums': Album.objects.all(),
        }
        return render(request, 'gallery_admin/home.html', context=context)
