from django.contrib import admin
from customers.models import Customer
from .models import DeliveryOrder
# Register your models here.

admin.site.register(Customer)
admin.site.register(DeliveryOrder)