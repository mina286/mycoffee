from django.shortcuts import redirect, render
from .models import UserProfile
from django.contrib.auth.models import User
from django.contrib import messages
import re
from django.contrib import  auth
from products.models import Product
# Create your views here.
def signin(request):
    if request.method=='POST' and 'btnsignin' in request.POST:
        if 'username' in request.POST and 'password' in request.POST:
            username = request.POST['username']
            password = request.POST['password']
            user=auth.authenticate(username=username,password=password)
            if user is not None:
                auth.login(request,user)
                if 'remember' not in request.POST: 
                    request.session.set_expiry(0)

                return redirect('index')

            else:
                messages.error(request,'error in username or password')

        else:
            messages.error(request,'check names')
      

    return render(request,'accounts/signin.html')

#logout def
def logout(request):
    auth.logout(request)
    return redirect('index')
# signup def
def signup(request):
    terms=None
    context = None
    is_added=False
    if request.method=='POST' and 'btnsignup' in request.POST:

        if  'terms' in request.POST:
            terms = request.POST['terms']

        if terms =='on':
            if 'fname' in request.POST and 'lname' in request.POST and 'address' in request.POST and 'address2' in request.POST and 'city' in request.POST and 'state' in request.POST and 'zip' in request.POST and 'email' in request.POST and 'username' in request.POST and 'pass' in request.POST :
                            fname =  request.POST['fname']
                            lname =  request.POST['lname']
                            address =  request.POST['address']
                            address2 =  request.POST['address2']
                            city =  request.POST['city']
                            state =  request.POST['state']
                            zip =  request.POST['zip']
                            email =  request.POST['email']
                            username =  request.POST['username']
                            password =  request.POST['pass']
                            patt="^\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$"
                            if re.match(patt,email):
                                if User.objects.all().filter(email=email).exists():
                                    messages.error(request,'please change email is exists')
                                else:
                                    if User.objects.all().filter(username=username).exists():
                                        messages.error(request,'please change username is exists')
                                    else:
                                        user = User.objects.create_user(
                                            username=username,
                                            first_name=fname,
                                            last_name=lname,
                                            email=email,
                                            password=password
                                        )
                                        user.save()
                                        userprofile= UserProfile()
                                        userprofile.address=address
                                        userprofile.address2=address2
                                        userprofile.city=city
                                        userprofile.state=state
                                        userprofile.zip_number=zip
                                        userprofile.user=user
                                        userprofile.save()
                                        is_added=True
                                        messages.success(request,'thank you for register .ok')

                            else:
                               
                                messages.error(request,'you shold write correct email')   
            else:
                messages.error(request,'please check names')

        else:
             messages.error(request,'you should agree term or check names term') 
             return render(request,'accounts/signup.html')
        context = {
                                            'fname':fname,
                                            'lname':lname,
                                            'address':address,
                                            'address2':address2,
                                            'city':city,
                                            'state':state,
                                            'zip':zip,
                                            'email':email,
                                            'username':username,
                                            'password':password,
                                            'is_added':is_added,
                                        }

    return render(request,'accounts/signup.html',context)



#def profile and remove profile
def profile(request):
    context = None
    fname = None
    lname = None
    address = None
    address2 = None
    city = None
    state = None
    zip= None
    email = None
    username = None
    password = None
   #modify in this account
    if request.method=='POST' and 'btnprofile' in request.POST:
        if 'fname' in request.POST and 'lname' in request.POST and 'address' in request.POST and 'address2' in request.POST and 'city' in request.POST and 'state' in request.POST and 'zip' in request.POST and 'email' in request.POST and 'username' in request.POST and 'pass' in request.POST :
            zip =request.POST['zip']
            if zip.isdigit() and len(zip)<6:
                userprofile = UserProfile.objects.get(user=request.user)
                request.user.first_name =  request.POST['fname']
                request.user.last_name =  request.POST['lname']
                userprofile.address =  request.POST['address']
                userprofile.address2 =  request.POST['address2']
                userprofile.city =  request.POST['city']
                userprofile.state =  request.POST['state']
                userprofile.zip_number =  request.POST['zip']
                request.user.email =  request.POST['email']
                request.user.username =  request.POST['username']
                if not request.POST['pass'].startswith('pbkdf2_sha256$320000$'):
                    password =  request.POST['pass']
                    request.user.set_password(password)
                request.user.save()
                userprofile.save()
                messages.success(request,'data has been changed')
            else:
                messages.error(request,'zip should be number and more 5 number')
        else:
            messages.error(request,'please check names')


    #remove account
    if request.method=='POST' and 'btnremoveprofile' in request.POST:
        userprofile = UserProfile.objects.get(user=request.user)
        userprofile.user.delete()

        return redirect('index')
    

    # show  account
    if request.user.is_authenticated and not request.user.is_anonymous:
        userprofile=UserProfile.objects.get(user=request.user)
        context = {
                                            'fname':userprofile.user.first_name,
                                            'lname':userprofile.user.last_name,
                                            'address':userprofile.address,
                                            'address2':userprofile.address2,
                                            'city':userprofile.city,
                                            'state':userprofile.state,
                                            'zip':userprofile.zip_number,
                                            'email':userprofile.user.email,
                                            'username':userprofile.user.username,
                                            'password':userprofile.user.password,
                             
                                        }
    return render(request,'accounts/profile.html',context)







#def product favorites
def product_favorite(request,pro_id):
    if request.user.is_authenticated and not request.user.is_anonymous:
        pro_fav=Product.objects.get(id=pro_id)
        #check pro is exist
        if  UserProfile.objects.all().filter(user=request.user,product_favorites=pro_fav).exists():
            messages.success(request,'you already added to list before ')
        # not exists           
        else:
            pro_id=pro_id
            userprofile = UserProfile.objects.get(user=request.user)
            userprofile.product_favorites.add(pro_fav)
            userprofile.save()   
            
            messages.success(request,'you added to list ')

   
    else:
        messages.error(request,'you should first login ')

    return redirect('/products/product/'+str(pro_id))



#remove product favorites
def remove_product_favorite(request):

    return render(request,'products/products.html')
#show product favorites
def show_prodcut_favorite(request):
    context=None
    pro=None
    is_fav=None
    pid_fav=None
    if request.user.is_authenticated and not request.user.is_anonymous:
        userprofile = UserProfile.objects.get(user=request.user)
        #show all product fav
        if userprofile.product_favorites.all():
            pro=userprofile.product_favorites.all()
            is_fav=True
        else:
            messages.error(request,'sorry no products favorites here')
        #remove poduct fav
        if 'btnremovefavid' in request.GET :
            pid_fav=request.GET['pid_fav']
            pro_fav=Product.objects.get(id=pid_fav)
            if UserProfile.objects.all().filter(user=request.user,product_favorites=pro_fav).exists():
                
                userprofile=UserProfile.objects.get(user=request.user,product_favorites=pro_fav)
                userprofile.product_favorites.remove(pro_fav)
                messages.success(request,'ok success remove')

            else:
                messages.error(request,'no favorites here after remove')

       

    else:
        messages.error(request,'you should first login ')
    context={
            'products':pro,
            'is_fav':is_fav
        }

    return render(request,'products/products.html',context)