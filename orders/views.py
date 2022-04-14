from django.shortcuts import redirect, render
from orders.models import Order
from orders.models import OrderDetails
from products.models import Product 
from django.contrib import messages
from orders.models import Payment
# Create your views here.


def add_to_cart(request):
    pro_id = request.GET['pro_id']
    if request.user.is_authenticated and not  request.user.is_anonymous:
        pro_id = request.GET['pro_id']
        if 'qty' in request.GET and 'pro_id' in request.GET:
            quantity = request.GET['qty']
            pro_id = request.GET['pro_id']

            pro=Product.objects.get(id=pro_id)

            #1 check exists any order for user
            if Order.objects.all().filter(user=request.user,is_finished=False).exists():
                #old_order
                if Order.objects.all().filter(user=request.user,is_finished=False).exists():
                    
                    order = Order.objects.get(user=request.user,is_finished=False)  
                    orderdetails =OrderDetails()
                    # check product ont add before
                    if OrderDetails.objects.all().filter(order=order,product=pro): 
                        messages.success(request,'this product is added before')
                    else:
                        orderdetails.product=pro
                        orderdetails.order = order 
                        orderdetails.price = pro.price
                        orderdetails.quantity=quantity
                        orderdetails.save()
                        messages.success(request,'added to old_order for you for order '+str(order.id))
                #new order
                

            else:
                order = Order()
                order.user=request.user
                order.save()

                orderdetails =OrderDetails()
                orderdetails.product=pro
                orderdetails.order = order
                orderdetails.price = pro.price
                orderdetails.quantity=quantity
                orderdetails.save()
                messages.success(request,'added to new_order for you first order')
        else:
            messages.error(request,'please check names ')
        return redirect('/products/product/'+str(pro_id))

    else:
        messages.error(request,'please login first  ')

    return redirect('/products/product/'+str(pro_id))

#show_cart
def show_cart(request):
    context =None
    if request.user.is_authenticated and not  request.user.is_anonymous:
        if Order.objects.all().filter(user=request.user,is_finished=False):
            order=Order.objects.get(user=request.user,is_finished=False)
            orderdetails=OrderDetails.objects.all().filter(order=order)
            #test total
            total=0
            for sub in orderdetails:   
                    total+=sub.price*sub.quantity
            #end test total
            if orderdetails:
                
                context={
                    'orderdetails':orderdetails,
                    'order':order,
                    'total':total,

                }
            else:
                 messages.error(request,'No products in cart Here')

            
        else:
            messages.error(request,'No products in cart Here')

    else:
        messages.error(request,'please login first')
    
    return render(request,'orders/cart.html',context)

#add quantity
def add_quantity(request,details_id):
    order=Order.objects.get(user=request.user,is_finished=False)
    orderdetails=OrderDetails.objects.get(order=order,id=details_id)
    orderdetails.quantity+=1
    orderdetails.save()
    return redirect('show_cart')
def sub_quantity(request,details_id):
    order=Order.objects.get(user=request.user,is_finished=False)
    orderdetails=OrderDetails.objects.get(order=order,id=details_id)
    if orderdetails.quantity>1:
        orderdetails.quantity-=1
        orderdetails.save()
    return redirect('show_cart')

#remove product
def remove_product(request,details_id):
    order=Order.objects.get(user=request.user,is_finished=False)
    orderdetails=OrderDetails.objects.get(order=order,id=details_id)
    orderdetails.delete()

    return redirect('show_cart')

#payment orders
def payment(request):
    context=None
    #user is authenticated
    if 'btnchek' in request.GET or 'btnchek' in request.POST:
        if request.method=='POST' and 'btnpayment' in request.POST:
            #order found
            if Order.objects.all().filter(user=request.user,is_finished=False).exists():
                #check names
                if 'pname' in request.POST and  'phone' in request.POST and 'cardnumber' in request.POST and  'expire' in request.POST and  'code' in request.POST :
                    pname= request.POST['pname']
                    phone= request.POST['phone']
                    cardnumber= request.POST['cardnumber']
                    expire= request.POST['expire']
                    code= request.POST['code']

                    order=Order.objects.get(user=request.user,is_finished=False)
                    payment = Payment()

                    payment.order=order
                    payment.personname=pname
                    payment.phone=phone
                    payment.cardnumber=cardnumber
                    payment.expire=expire
                    payment.code=code
                    order.is_finished=True
                    payment.save()
                    order.save()
                    context={
                        'order':order
                                            }
                    messages.success(request,'thank you for order godluck')

                #names not found
                else:
                     messages.error(request,'please check names')
            #orders not found
            else:
                messages.error(request,'no orders to payment it here')

    #user anonymous  
    else:
        messages.error(request,'you shoud login first ')
        context = {
            'order':'anonymous'
        }
   

    return render(request,'orders/payment.html',context)
#show_orders
def show_orders(request):
    context=None
    order=None
    items_count=0
    if request.user.is_authenticated and not request.user.is_anonymous:
        
        # check order exists
            order=Order.objects.all().filter(user=request.user)
            # check exists
            if order:
              
            #هيروج بخزن فى كل مره بيانات الاورد ده وانا عامل كده فى الموديلshow order
                for x in order:
                
                    one_order=Order.objects.get(id=x.id)
                    orderdetails =OrderDetails.objects.all().filter(order=one_order)
                    total=0
                    for sub in orderdetails:
                        total+=sub.quantity*sub.price
                    x.total=total
                    x.items_count=orderdetails.count
                    items_count=x.items_count
              
                #remove this order
                if 'btnremoveorder' in request.POST:
                    id_orderremove=request.POST['id_orderremove']
                    rorder = Order.objects.get(id=id_orderremove)
                    rorder.delete()

           

    else:
        messages.error(request,'you shoud login first ')
  
   
    context={
                'order':order,
                'items_count': items_count
                    }
    
    return render(request,'orders/show_orders.html',context)