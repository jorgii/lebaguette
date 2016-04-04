from django.forms import ModelForm
from django.contrib.auth.models import User

from .models import ServerMessage


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class ServerMessageForm(ModelForm):
    class Meta:
        model = ServerMessage
        fields = ['message']
