from django.urls import path

from .views import HomeAdminView

app_name = 'gallery_admin'

urlpatterns = [
    path('', HomeAdminView.as_view(), name='home'),
]
