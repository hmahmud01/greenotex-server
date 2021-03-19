from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required

import json
from ecommerce.models import MainBuyer, Brand, Product, CompanyInfo, CustomerDetail, Localbuyer
from ecommerce.models import Order, OrderItems, ShippingAddress, DelivaryAddress, BillingAddress
from .utils import cartData

@login_required(login_url="/login/")
def home(request):
    data = ""
    if request.user.is_authenticated:
        localbuyer = Localbuyer.objects.get(user_id=request.user.id)
        localbuyer_brand_id = localbuyer.company_info.brands.id        
        mainbuyer = MainBuyer.objects.get(id=localbuyer_brand_id)
        data = mainbuyer
        cartItems = Order.get_cart_items
    return render(request, 'index.html', {'data': data, 'cartItems': cartItems})

@login_required
def addresses(request):
    delivery = DelivaryAddress.objects.all()
    billing = BillingAddress.objects.all()
    return render(request, 'addresses.html', {'delivery': delivery, 'billing': billing})

@login_required
def addDeliveryAddress(request):
    post_data = request.POST
    user = request.user
    buyer = Localbuyer.objects.get(user_id=user.id)
    address = DelivaryAddress(
        user = buyer,
        street = post_data['street'],
        city = post_data['city'],
        zipcode = post_data['zipcode'],
        country = post_data['country'],
    )

    address.save()
    return redirect('addresses')

@login_required
def addBillingAddress(request):
    post_data = request.POST
    user = request.user
    buyer = Localbuyer.objects.get(user_id=user.id)
    address = BillingAddress(
        user = buyer,
        street = post_data['street'],
        city = post_data['city'],
        zipcode = post_data['zipcode'],
        country = post_data['country'],
    )

    address.save()
    return redirect('addresses')

@login_required(login_url="/login/")
def categories(request):        
    brands = Brand.objects.filter(mainbuyer_id=1)    
    cartItems = Order.get_cart_items
    return render(request, 'categories.html', {'brands': brands, 'cartItems': cartItems})

def filteredCategory(request, cid):
    brands = Brand.objects.filter(mainbuyer_id=cid)    
    cartItems = Order.get_cart_items
    return render(request, 'categories.html', {'brands': brands, 'cartItems': cartItems})

def login(request):
    data = ""
    return render(request, 'login.html', {'data': data})

def signup(request):
    mainbuyer = MainBuyer.objects.all()
    return render(request, 'signup.html', {'mainbuyer': mainbuyer})

def createlocalbuyer(request):
    print(request.POST)
    post_data = request.POST
    default_pass = "greeontexuser2021"
    user = User.objects.create_user(post_data['email'], post_data['email'], default_pass)
    mainbuyer_id = post_data['mainbuyer_id']
    brand = MainBuyer.objects.get(id=mainbuyer_id)

    agent_info = False
    if post_data['agent'] == "yes":
        agent_info = True

    companyInfo = CompanyInfo(
        account = post_data['account'],
        company = post_data['company_name'],
        street_english = post_data['street_english'],
        street_chinese = post_data['street_chinese'],
        country = post_data['country'],
        city = post_data['city'],
        postal_code = post_data['postal'],
        accounting_attention_person = post_data['accounting_attention_person'],
        account_email = post_data['accounting_email'],
        purchase_attention_person = post_data['purchase_attention_person'],
        purchase_email = post_data['purchase_email'],
        phone = post_data['phone'],
        fax = post_data['fax'],
        vat = post_data['vat'],
        brands = brand,
        is_agent = agent_info,
    )

    companyInfo.save()

    customerDetail = CustomerDetail(
        company = post_data['company_customer'],
        contact_person = post_data['contact_person'],
        contact_email = post_data['contact_email'],
        order_number = post_data['order_number'],
        supplier_code = post_data['supplier_code'],
    )

    customerDetail.save()

    localBuyer = Localbuyer(
        user = user,
        status = False,
        name = post_data['name'],
        company_info = companyInfo,
        customer_detail = customerDetail,
    )

    localBuyer.save()
    return redirect('accounthalt')

def accountHalt(request):
    data = ""
    return render(request, 'inactive.html', {'data': data})

def verifylogin(request):
    post_data = request.POST
    if 'user' and 'pass' in post_data:
        user = authenticate(
            request,
            username = post_data['user'],
            password = post_data['pass']
        )
        if user is None:
            return redirect('login')
        elif user.is_superuser:
            auth_login(request, user)
            return redirect('dashboard')
        else:
            localbuyer = Localbuyer.objects.get(user_id=user.id)
            if localbuyer.status == False:
                return redirect('accounthalt')    
            else:                
                auth_login(request, user)            
                return redirect('/')

def activatelocalbuyer(request, uid):
    localbuyer = Localbuyer.objects.get(id=uid)
    localbuyer.status = True
    localbuyer.save()
    return redirect('localbuyer')

def deactivatelocalbuyer(request, uid):
    localbuyer = Localbuyer.objects.get(id=uid)
    localbuyer.status = False
    localbuyer.save()
    return redirect('localbuyer')

def userLogout(request):
    logout(request)
    return redirect('login')

@login_required(login_url="/login/")
def productlist(request,bid):
    products = Product.objects.filter(brand_id=bid)
    cartItems = Order.get_cart_items
    return render(request, 'productlist.html', {'products': products, 'cartItems': cartItems})

@login_required(login_url="/login/")
def productdetail(request, pid):
    product = Product.objects.get(id=pid)
    price_usd = product.price
    price_rmb = price_usd * 6.47
    price_bdt = price_usd * 84.80
    cartItems = Order.get_cart_items
    return render(request, 'productdetail.html', {'product': product, 'price_usd': price_usd, 'price_rmb':price_rmb, 'price_bdt': price_bdt, 'cartItems': cartItems})

# Dashboard views
@login_required(login_url="/login/")
def dashboard(request):
    data = ""
    return render(request, 'dashboard.html', {'data': data})

def products(request):
    mainbuyer = MainBuyer.objects.all()
    products = Product.objects.all()
    return render(request, 'dashboard_products.html', {'mainbuyer': mainbuyer, 'products': products})

def brandfind(request):
    pass

def brands(request):
    brands = Brand.objects.all()
    mainbuyer = MainBuyer.objects.all()
    return render(request, 'brands.html', {'brands': brands, 'mainbuyer': mainbuyer})

def localbuyer(request):
    data = Localbuyer.objects.all()    
    return render(request, 'buyer_local.html', {'data': data})

def mainbuyer(request):
    data = MainBuyer.objects.all()
    return render(request, 'buyer_main.html', {'data': data})

def savemainbuyer(request):
    post_data = request.POST

    mainbuyer = MainBuyer(
        name = post_data['name'],
        email = post_data['email']
    )

    mainbuyer.save()

    return redirect('mainbuyer')

def savebrand(request):
    post_data = request.POST

    mainbuyer_id = post_data['mainbuyer']
    mainbuyer = MainBuyer.objects.get(id=mainbuyer_id)

    brand = Brand(
        name = post_data['name'],
        mainbuyer = mainbuyer
    )

    brand.save()

    return redirect('brands')

def loadbrand(request):
    mainbuyer_id = request.GET.get('mainbuyer_id')
    brands = Brand.objects.filter(mainbuyer_id=mainbuyer_id).order_by('name')
    return render(request, 'brandsajax.html', {'brands': brands})

def saveproduct(request):
    post_data = request.POST
    brand_id = post_data['id_brand']
    brand = Brand.objects.get(id=brand_id)

    product = Product(
        title = post_data['title'],
        brand = brand,
        description = post_data['description'],
        price = post_data['price'],
        photo = request.FILES['photo']
    )

    product.save()

    return redirect('products')

def cart(request):
	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']
	context = {'items':items, 'order':order, 'cartItems':cartItems}    
	return render(request, 'cart.html', context)

def checkout(request):
	data = cartData(request)	
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']
	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'checkout.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action : ', action)
    print('productId : ', productId)

    customer = request.user.localbuyer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItems.objects.get_or_create(order=order, product=product)
    
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)



