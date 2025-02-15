from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauths.models import User, Profile

class UserRegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Username'}))
    User_Email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':'Email'}), error_messages={'unique':'This email address is already in use. Please choose a different one.'})
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password'}))
    
    class Meta:
        model = User
        fields = [
            'username',
            'User_Email'
        ]

class ProfileForm(forms.ModelForm):
    full_name = forms.CharField(label='Full Name', widget=forms.TextInput(attrs={'placeholder':'Full Name'}))
    bio = forms.CharField(label='Bio', widget=forms.TextInput(attrs={'placeholder':'Bio'}))
    phone = forms.CharField(label='Phone', widget=forms.TextInput(attrs={'placeholder':'Phone'}))
    image = forms.ImageField()
    class Meta:
        model = Profile
        fields = ['full_name', 'image', 'bio', 'phone']