from django import views
from django.urls import path
from . import views
urlpatterns = [
path('add_to_cart',views.add_to_cart,name="add_to_cart"),
path('show_cart',views.show_cart,name="show_cart"),
path('add_quantity/<int:details_id>',views.add_quantity,name="add_quantity"),
path('sub_quantity/<int:details_id>',views.sub_quantity,name="sub_quantity"),
path('remove_product/<int:details_id>',views.remove_product,name="remove_product"),
path('payment',views.payment,name="payment"),
path('show_orders',views.show_orders,name="show_orders"), 
  
] 