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
        