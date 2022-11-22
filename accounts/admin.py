from django.contrib import admin

# Register your models here.
from accounts.models import Account, Item, Vendor

admin.site.register(Account)
admin.site.register(Item)
admin.site.register(Vendor)
