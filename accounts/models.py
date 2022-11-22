from django.db import models

# Create your models here.
class Account(models.Model):
    nama = models.CharField(max_length=200, null=True)
    deskripsi = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self) -> str:
        return self.nama