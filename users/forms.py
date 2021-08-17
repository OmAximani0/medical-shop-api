from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Users
from django import forms

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = Users
        fields = ('user_name','user_email')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = Users
        fields = ('user_name','user_email')