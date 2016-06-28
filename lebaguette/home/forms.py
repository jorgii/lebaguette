from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm

from .models import ServerMessage


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = \
            "mdl-textfield__input"
        self.fields['first_name'].widget.attrs['class'] = \
            "mdl-textfield__input"
        self.fields['last_name'].widget.attrs['class'] = \
            "mdl-textfield__input"
        self.fields['email'].widget.attrs['class'] = \
            "mdl-textfield__input"


class ServerMessageForm(ModelForm):
    class Meta:
        model = ServerMessage
        fields = ['message']


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(CustomAuthenticationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = "mdl-textfield__input"
        self.fields['username'].widget.attrs['required'] = True
        self.fields['password'].widget.attrs['class'] = "mdl-textfield__input"
        self.fields['password'].widget.attrs['required'] = True


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(CustomPasswordChangeForm, self).__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs['class'] = \
            "mdl-textfield__input"
        self.fields['new_password1'].widget.attrs['class'] = \
            "mdl-textfield__input"
        self.fields['new_password2'].widget.attrs['class'] = \
            "mdl-textfield__input"
