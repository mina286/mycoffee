from dataclasses import fields
from django.contrib import admin
from products.models import Product
# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display=['name','price','is_active'] 
    list_display_links = ['price','is_active']
    list_editable=['name']
    search_fields=['price'] 
    list_filter=['price','is_active'] 
    fields=['name','price']
admin.site.register(Product,ProductAdmin)
