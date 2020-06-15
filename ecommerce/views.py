from django.shortcuts import render, redirect
from .models import *
import csv, io 
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib import messages
from .models import Shipping

# Create your views here.
def logout(request):
    auth.logout(request)
    return redirect('dashboard')

def login(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('dashboard')
        else:
            messages.info(request,'Invalid Username/Password.')
            return redirect('login')

    return render(request,'ecommerce/login.html')

def register(request):

    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username Already Exists')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'Email Already Exists')
                return redirect('register')  
            else:      
                user = User.objects.create_user(username = username,password=password1,email=email,first_name=first_name,last_name=last_name)
                user.save()
                print('user created.')
                return redirect('login')
        else:
            messages.info(request,'Password Not Match!')
            return redirect('register')

        

    else:    
        return render(request,'ecommerce/register.html')

def sample(request):
    locations = Location.objects.all()
    context = {'locations':locations}
    return render(request,'ecommerce/sample.html',context)

def dashboard(request):

    if 'cart' not in request.session:
        request.session['cart'] = []

    cart = request.session['cart']
    request.session.set_expiry(0)    

    if request.method == 'POST':
        cart.append(int(request.POST['obj_id']))
        return redirect('dashboard')

    products = Product.objects.all()
    context = {'products':products}
    # if request.method == "POST":
    #     return redirect('cart')

    return render(request,'ecommerce/dashboard.html',context)

def checkout(request):
    if request.method == 'POST':
        customer = request.user.customer
        address = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        zipcode = request.POST['zipcode']

        shipping = Shipping.objects.create(customer= customer, address = address,city = city, state = state, zipcode = zipcode)
        shipping.save()
        messages.success(request,"You will receive your order soon..")
        return redirect('/')


    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer)
        items = order.orderitem_set.all()
    else:
        items = [] 
        order = {'total_cart_fruits':0 ,'total_cart_price':0} 


    
    
    context ={'items':items,'order':order}
    return render(request,'ecommerce/checkout.html',context)       

# @login_required(login_url='login')
def cart(request):
    cart = request.session['cart']
    request.session.set_expiry(0)
    
    if request.user.is_authenticated:
        
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer)
        items = order.orderitem_set.all()
    else:
        items = [] 
        order = {'total_cart_fruits':0 ,'total_cart_price':0} 
    
    context ={'items':items,'order':order, 'cart':cart}
    return render(request,'ecommerce/cart.html',context)


def maps(request):
    return render(request,'ecommerce/map.html')


@permission_required('admin_can_add_log_entry')
def location_upload(request):
    prompt = {
        'order':'Order of CSV should be state, city, latitude,longitude,farm'
    }    

    if request.method == 'GET':
        return render(request,'ecommerce/location_upload.html',prompt)

    csv_file = request.FILES['file']
    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'This is not a csv file')    

    data_set = csv_file.read().decode('unicode_escape')
    io_string = io.StringIO(data_set)
    next(io_string) 

    for column in csv.reader(io_string, delimiter= ',', quotechar="|"):
        _, created = Location.objects.update_or_create(
            state = column[0],
            city = column[1],
            latitude = column[2],
            longitude = column[3],
            farm = column[4]
        )  

    context = {}
    return render(request,'ecommerce/location_upload.html',context)