from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Vendor, Service, Contact, Contract

admin.site.register(Vendor)
admin.site.register(Service)
admin.site.register(Contact)
admin.site.register(Contract)
