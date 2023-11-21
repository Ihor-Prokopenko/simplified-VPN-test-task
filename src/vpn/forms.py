from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django import forms

from .models import User
from vpn.models import Site


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label='Email',
                             widget=forms.TextInput(attrs={'class': 'form-control text-center', 'placeholder': 'email',
                                                           'style': 'max-width: 300px; margin: 0 auto;'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'bio')

        labels = {
            'bio': 'Bio (optional)',
        }

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control text-center'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].widget.attrs['style'] = 'max-width: 300px; margin: 0 auto;'
        self.fields['password1'].widget.attrs['class'] = 'form-control text-center'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].widget.attrs['style'] = 'max-width: 300px; margin: 0 auto;'
        self.fields['password2'].widget.attrs['class'] = 'form-control text-center'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].widget.attrs['style'] = 'max-width: 300px; margin: 0 auto;'
        self.fields['bio'].widget.attrs['class'] = 'form-control'
        self.fields['bio'].widget.attrs['placeholder'] = 'Write something about yourself'
        self.fields['bio'].widget.attrs['style'] = 'max-width: 300px; margin: 0 auto; height: 50px;'


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Login')
    password = forms.PasswordInput()

    def __init__(self, *args, **kwargs):
        super(LoginUserForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control text-center'
        self.fields['username'].widget.attrs['style'] = 'max-width: 300px; margin: 0 auto;'
        self.fields['password'].widget.attrs['class'] = 'form-control text-center'
        self.fields['password'].widget.attrs['style'] = 'max-width: 300px; margin: 0 auto;'


class CreateSiteForm(forms.ModelForm):
    class Meta:
        model = Site
        fields = ['name', 'base_url']
        labels = {
            'base_url': 'Original URL',
        }

    def __init__(self, *args, **kwargs):
        super(CreateSiteForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['class'] = 'form-control text-center'
        self.fields['name'].widget.attrs['style'] = 'max-width: 300px; margin: 0 auto;'
        self.fields['base_url'].widget.attrs['class'] = 'form-control text-center'
        self.fields['base_url'].widget.attrs['style'] = 'max-width: 300px; margin: 0 auto;'

    def clean_name(self):
        """
        This method checks if the name contains only alphanumeric characters. If it contains any
        non-alphanumeric characters, a ValidationError is raised.

        Returns:
            str: The cleaned name.

        Raises:
            ValidationError: If the name contains non-alphanumeric characters.
        """
        name = self.cleaned_data['name']
        if not name.isalnum():
            raise ValidationError("Name can only contain letters and numbers.")
        return name


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'bio']
        labels = {
            'username': 'Username',
            'email': 'Email',
            'bio': 'Bio',
        }
        help_texts = {
            'username': ' ',
        }

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)

        self.fields['bio'].widget.attrs['class'] = 'form-control'
        self.fields['bio'].widget.attrs['style'] = 'max-width: 300px; margin: 0 auto;'
        self.fields['username'].widget.attrs['class'] = 'form-control text-center'
        self.fields['username'].widget.attrs['style'] = 'max-width: 300px; margin: 0 auto;'
        self.fields['email'].widget.attrs['class'] = 'form-control text-center'
        self.fields['email'].widget.attrs['style'] = 'max-width: 300px; margin: 0 auto;'
