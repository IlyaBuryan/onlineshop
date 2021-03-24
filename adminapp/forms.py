from django.contrib.auth import get_user_model
from authapp.forms import EditForm, UserCreationForm


class ShopUserAdminUpdateForm(EditForm):
    class Meta:
        model = get_user_model()
        exclude = ('user_permissions', 'groups', 'last_login', 'email', 'activ_key', 'activ_key_expires')


class ShopUserAdminCreateForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        exclude = ('user_permissions', 'groups', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.help_text = ''

    def clean(self):
        cleaned_data = super().clean()
        age = cleaned_data['age']

        if age < 18 or age > 150:
            self.add_error('age', 'Check the age. 18 is the minimum.')
