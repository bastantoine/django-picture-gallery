from django.forms import ModelForm

from apps.core.models import Album


class AlbumForm(ModelForm):
    class Meta:
        model = Album
        fields = ['name', 'start_date', 'end_date', 'parent_album', 'description', 'is_protected']
