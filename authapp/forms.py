from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm, forms


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class RegisterForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = [
            'username',
            'password1',
            'password2',
            'first_name',
            'last_name',
            'email',
            'age',
            'city',
            'avatar'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.help_text = ''

    def clean(self):
        cleaned_data = super().clean()
        age = cleaned_data['age']

        if age < 18 or age > 150:
            self.add_error('age', 'Check the age. 18 is the minimum.')


class EditForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name', 'email', 'age', 'city', 'avatar']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.help_text = ''
            if field_name == 'password':
                field.widget = forms.HiddenInput()
            if field_name == 'avatar':
                field.widget.initial_text = ''
                field.widget.input_text = ''
                field.widget.clear_checkbox_label = ''

    def clean(self):
        cleaned_data = super().clean()
        age = cleaned_data['age']

        if age < 18 or age > 150:
            self.add_error('age', 'Check the age. 18 is the minimum.')
