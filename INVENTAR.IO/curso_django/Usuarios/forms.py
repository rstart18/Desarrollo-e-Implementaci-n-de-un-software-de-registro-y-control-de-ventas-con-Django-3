from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreation(UserCreationForm):

    class Meta:
        model = User
        fields = ['first_name','last_name','email','username','password1','password2']

class CustomUserEdit(ModelForm):

    class Meta:
        model = User
        fields = ['first_name','last_name','email','username']