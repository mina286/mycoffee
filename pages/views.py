from django.shortcuts import render,redirect
from django.http import HttpResponse
from products.models import Product
# Create your views here.
def index(request):
    context =None
    pro=Product.objects.all()
    context ={
        'products':pro
    }
    return render(request,'pages/index.html',context)
def coffee(request):
    return render(request,'pages/coffee.html')
def about(request):
    return render(request,'pages/about.html')
