from .models import Comment
from django.forms import ModelForm
from django.contrib.auth.forms import forms

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == 'comment':
                field.widget.attrs['placeholder'] = 'Type text here'
            if field_name == 'user':
                field.widget = forms.HiddenInput()
            if field_name == 'product':
                field.widget = forms.HiddenInput()
