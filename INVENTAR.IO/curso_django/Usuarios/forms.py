from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import User,CreditCards

class CustomUserCreation(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','email','username','cedula','password1','password2']

class CustomUserEdit(ModelForm):

    class Meta:
        model = User
        fields = ['first_name','last_name','email','username','cedula']

class AddCreditCard(ModelForm):

    class Meta:
        model = CreditCards
        fields = ['cc','mes_de_vencimiento','año_de_vencimiento','ccv']