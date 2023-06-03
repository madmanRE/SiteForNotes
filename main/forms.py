from django.forms import ModelForm
from django import forms
from .models import Profile, Note


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=100, help_text="имя пользователя")
    password = forms.CharField(required=True, help_text="пароль")


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('username', 'avatar',)


class NoteForm(ModelForm):
    class Meta:
        model = Note
        fields = ('title', 'text', 'theme', 'importance', 'color')



