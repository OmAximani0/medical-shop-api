from django.contrib import admin

from .models import Order, OrderMedicine

admin.site.register(OrderMedicine)
admin.site.register(Order)