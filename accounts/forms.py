from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm

class UserCustomCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name',)