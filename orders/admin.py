from django.contrib import admin
from orders.models import Order
from orders.models import OrderDetails
from orders.models import Payment
# Register your models here.
admin.site.register(Order)
admin.site.register(OrderDetails) 
admin.site.register(Payment) 