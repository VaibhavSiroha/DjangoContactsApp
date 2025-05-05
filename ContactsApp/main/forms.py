from django.forms import ModelForm
from .models import Contact
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class ContactForm(forms.ModelForm):
    class Meta:
        model=Contact
        fields=['name','email','number']

class EditForm(forms.ModelForm):
    class Meta:
        model=Contact
        fields=['name','email','number']

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'number')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'number')
