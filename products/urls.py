from unicodedata import name
from django.urls import path
from . import views

urlpatterns =[
   
   path('',views.products,name="products"),
   path('product/<int:pro_id>',views.product,name="product"),
   path('search',views.search,name="search"),
]