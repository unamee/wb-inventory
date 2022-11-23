from django.contrib import admin

# Register your models here.
from accounts.models import *

admin.site.register(Account)
admin.site.register(Item)
admin.site.register(Vendor)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
