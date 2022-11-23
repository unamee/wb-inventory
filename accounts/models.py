from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Account(models.Model): # customer
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE, blank=True)
    nama = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    deskripsi = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self) -> str:
        return self.nama
    
class Item(models.Model): # product
    nama = models.CharField(max_length=200, null=True)
    deskripsi = models.CharField(max_length=200, null=True)
    price = models.FloatField(null=True, blank=True, default=False)
    digital = models.BooleanField(default=False, null=True, blank=False)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    image = models.ImageField(null=True, blank=True)
    
    def __str__(self) -> str:
        return self.nama
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    
class Vendor(models.Model):
    nama = models.CharField(max_length=200, null=True)
    deskripsi = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self) -> str:
        return self.nama
    
class Order(models.Model):
    account = models.ForeignKey(Account, on_delete=models.SET_NULL, blank=True, null=True)
    date_orderd = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)
    
    def __str__(self) -> str:
        return str(self.id)
    
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
    
class OrderItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    @property
    def get_total(self):
        total = self.item.price * self.quantity
        return total
    
class ShippingAddress(models.Model):
    account = models.ForeignKey(Account, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.nama
    