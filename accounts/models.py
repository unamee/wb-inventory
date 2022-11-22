from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Account(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    nama = models.CharField(max_length=200, null=True)
    deskripsi = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self) -> str:
        return self.nama
    
class Item(models.Model):
    nama = models.CharField(max_length=200, null=True)
    deskripsi = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self) -> str:
        return self.nama
    
class Vendor(models.Model):
    nama = models.CharField(max_length=200, null=True)
    deskripsi = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self) -> str:
        return self.nama