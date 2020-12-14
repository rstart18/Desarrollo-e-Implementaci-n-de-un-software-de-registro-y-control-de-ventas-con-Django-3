from django import forms
from .models import Productos,Proveedores,Categorias

class SupplyForm(forms.ModelForm):

    class Meta:
        model = Productos
        fields = ['units']

class ProductCreationForm(forms.ModelForm):

    class Meta:
        model = Productos
        fields = ['name','units','reference','enter_price','exit_price','Proveedor','Categoria','imagen']

class ProductEditForm(forms.ModelForm):

    class Meta:
        model = Productos
        fields = ['name','units','enter_price','exit_price','Proveedor','Categoria','imagen']


class ProviderCreationForm(forms.ModelForm):

    class Meta:
        model = Proveedores
        fields = ['enterprise_name','reference','telephone','email','address']


class ProviderEditForm(forms.ModelForm):

    class Meta:
        model = Proveedores
        fields = ['enterprise_name','telephone','email','address']


class CategoryCreationForm(forms.ModelForm):

    class Meta:
        model = Categorias
        fields = ['name','reference']

class CategoryEditForm(forms.ModelForm):

    class Meta:
        model = Categorias
        fields = ['name']