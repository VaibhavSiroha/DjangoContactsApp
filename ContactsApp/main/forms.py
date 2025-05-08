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

class OtpForm(forms.Form):
    otp = forms.CharField(
        max_length=6,
        min_length=6,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Enter 6-digit OTP'}),
        error_messages={'required': 'OTP is required.'}
    )