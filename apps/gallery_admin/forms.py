from django.forms import Form, ModelForm, ClearableFileInput, DateInput, PasswordInput
from django.forms.fields import CharField

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from apps.core.models import Album, Picture


def form_helper(form_action, submit_label, form_id=None):
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.form_method = 'post'
    helper.form_action = form_action
    helper.label_class = 'col-lg-2'
    helper.field_class = "col-lg-10"
    if form_id:
        helper.form_id = form_id
    helper.add_input(Submit('submit', submit_label))
    return helper


class AlbumForm(ModelForm):
    class Meta:
        model = Album
        fields = ['name', 'start_date', 'end_date', 'parent_album', 'description', 'is_protected']
        widgets = {
            'start_date': DateInput(attrs={'type': 'date'}),
            'end_date': DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, form_action, submit_label, *args, **kwargs):
        form_id = kwargs.pop('form_id', None)
        super().__init__(*args, **kwargs)
        self.helper = form_helper(form_action, submit_label, form_id=form_id)


class PictureForm(ModelForm):
    class Meta:
        model = Picture
        fields = '__all__'
        widgets = {
            'path': ClearableFileInput(attrs={'multiple': True}),
        }

    def __init__(self, form_action, submit_label, *args, **kwargs):
        form_id = kwargs.pop('form_id', None)
        super().__init__(*args, **kwargs)
        self.helper = form_helper(form_action, submit_label, form_id=form_id)


class LoginForm(Form):
    username = CharField()
    password = CharField(widget=PasswordInput)

    def __init__(self, form_action, submit_label, *args, **kwargs):
        form_id = kwargs.pop('form_id', None)
        super().__init__(*args, **kwargs)
        self.helper = form_helper(form_action, submit_label, form_id=form_id)
