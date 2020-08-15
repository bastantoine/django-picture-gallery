from django.shortcuts import render
from django.views import View

from .models import Album


class HomeView(View):

    def get(self, request):
        context = {
            'albums': Album.objects.all(),
        }
        return render(request, 'viewer/home.html', context=context)
