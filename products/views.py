from email.mime import image
from django.shortcuts import redirect, render,get_object_or_404
from products.models import Product
from django.contrib import messages
# product
def product(request,pro_id):
    context=None
    pro = Product.objects.get(id=pro_id)
    context = {
        'pro':pro
    }
    return render(request,'products/product.html',context)

# all products

def products(request):
    context = None
    pname=None
    desc=None
    price_from=None
    price_to=None
    cs=None
    pro=Product.objects.all()
    
    if  'btnfastsearch' in request.GET :
        if  'pname' in  request.GET:
                pname=request.GET['pname']
                pro =Product.objects.all().filter(name__icontains=pname)
        else:
                messages.error(request,'please check names')
                return redirect('search')
    


    if 'btnsearch' in request.GET  :
        if  'pname' in  request.GET or 'desc' in request.GET or  'price_from' in request.GET or 'price_to' in request.GET:
           
            pname=request.GET['pname']
            
            desc=request.GET['desc']
            price_from=request.GET['price_from']
            price_to=request.GET['price_to']
            if  price_from.isdigit() and price_to.isdigit():
                if 'cs' in request.GET:
                        pro = Product.objects.all().filter(name__contains=pname,description__contains=desc,price__gte=price_from,price__lte=price_to)
                else:
                        pro =Product.objects.all().filter(name__icontains=pname,description__icontains=desc,price__gte=price_from,price__lte=price_to)
        else:
                messages.error(request,'please check names')
                return redirect('search')
    context ={
        'products':pro
        }
    return render(request,'products/products.html',context)

def search(request):
 

    return render(request,'products/search.html')

