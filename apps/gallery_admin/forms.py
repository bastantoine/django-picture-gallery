from django.forms import ModelForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from apps.core.models import Album


class AlbumForm(ModelForm):
    class Meta:
        model = Album
        fields = ['name', 'start_date', 'end_date', 'parent_album', 'description', 'is_protected']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.form_action = 'gallery_admin:add_album'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = "col-lg-10"
        self.helper.add_input(Submit('submit', 'Add album'))
