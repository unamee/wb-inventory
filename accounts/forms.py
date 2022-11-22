#from django.forms import ModelForm
from django import forms
from accounts.models import Account
from django.contrib.auth.models import User

class StaffForm(forms.ModelForm):    
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name']
        
class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['nama', 'deskripsi']
        
class PurchaseForm(forms.Form):
    nama = forms.CharField(max_length=100)  
    deskripsi_item = forms.CharField(max_length=100, disabled=True)
    product_number = forms.CharField(max_length=50, disabled=True)
    qty = forms.IntegerField()
    satuan = forms.CharField(max_length=3, disabled=True)    