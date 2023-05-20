from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import slider,Main_Category, Product, Category, Color, Brand, Review, Order
from django.http import JsonResponse
from .models import Vendor, VendorManager
from django.template.loader import render_to_string
from django.db.models import Max, Min, Sum, F, IntegerField
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from django.contrib import messages
from .forms import VendorCreationForm, VendorChangeForm, ReviewForm
from django.conf import settings
from django.urls import reverse
from django.db.models.functions import Cast
from decimal import Decimal, ROUND_HALF_UP
from django.shortcuts import get_object_or_404

def BASE(request):
    return render (request, 'commerce/base.html') 

def HOME(request):
    sliders = slider.objects.all()
    main_category = Main_Category.objects.all().order_by('-id')
    product = Product.objects.filter(section__name = "Top & Haughty Deals")
    
    
    context = {
        'sliders':sliders,
        'main_category':main_category,
        'product':product,
    }
    
    return render(request, 'commerce/home.html', context)



def add_money(request):
    if request.method == 'POST':
        amount = float(request.POST['amount'])
        request.session['wallet_balance'] = request.session.get('wallet_balance', 0) + amount
        return redirect('wallet')

    return render(request, 'commerce/add_money.html')

def wallet(request):
    wallet_balance = request.session.get('wallet_balance', 0)
    return render(request, 'commerce/wallet.html', {'wallet_balance': wallet_balance})


def PRODUCT_DETAILS(request, slug):
    product = Product.objects.filter(slug = slug)
    if product.exists():
        product = Product.objects.get(slug = slug)
    else:
        return redirect('404')
    
    context = {
        'product':product,
    }
    
    return render(request, 'commerce/product_detail.html', context)

def Error404(request):
    return render(request, 'commerce/errors/404.html')

def about(request):
    return render(request, 'commerce/about.html')

def contact(request):
    return render(request, 'commerce/contact.html')

@login_required(login_url="/login/")
def product(request):
    category = Category.objects.all()
    product = Product.objects.all()
    color = Color.objects.all()
    brand = Brand.objects.all()
    min_price = Product.objects.all().aggregate(Min('price'))
    max_price = Product.objects.all().aggregate(Max('price'))
    FilterPrice = request.GET.get('FilterPrice')
    ColorID = request.GET.get('colorID')
    sort_by = request.GET.get('sort_by')

    if FilterPrice:
        Int_FilterPrice = int(FilterPrice)
        product = Product.objects.filter(price__lte = Int_FilterPrice)
    elif ColorID:
        product = Product.objects.filter(color = ColorID)
    else:
        product = Product.objects.all()
       
    if sort_by == 'sales':
        product = sorted(product, key=lambda p: p.total_quantity - p.Availability, reverse=True)
        
    context = {
        'category':category,
        'product':product,
        'min_price':min_price,
        'max_price':max_price,
        'FilterPrice':FilterPrice,
        'color':color,
        'brand':brand,
        'sort_by': sort_by,
    }
    return render(request, 'commerce/product.html', context)

def filter_data(request):
    categories = request.GET.getlist('category[]')
    brands = request.GET.getlist('brand[]')
    brand = request.GET.getlist('brand[]')
    sort_by = request.GET.get('sort_by')

    allProducts = Product.objects.all().order_by('-id').distinct()
    if len(categories) > 0:
        allProducts = allProducts.filter(Categories__id__in=categories).distinct()

    if len(brands) > 0:
        allProducts = allProducts.filter(Brand__id__in=brands).distinct()
        
    if sort_by == 'sales':
        allProducts = sorted(allProducts, key=lambda p: p.total_quantity - p.Availability, reverse=True)

    t = render_to_string('commerce/ajax/product.html', {'product': allProducts})

    return JsonResponse({'data': t})

def submit_review(request, slug):
    product = get_object_or_404(Product, slug=slug)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            return redirect('product_detail', slug=slug)
    else:
        form = ReviewForm()
    
    context = {
        'form': form,
        'product': product,
    }
    
    return render(request, 'commerce/submit_review.html', context)

@login_required(login_url="/login/")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/login/")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/login/")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/login/")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/login/")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/login/")
def cart_detail(request):
    cart = request.session.get('cart')
    tax = sum(i['tax'] for i in cart.values() if i)
    delivery_charge = sum(i['delivery_charge'] for i in cart.values() if i)
    
    context = {
        'tax' : tax,
        'delivery_charge' : delivery_charge,
    }
    return render(request, 'commerce/cart.html', context)

def checkout(request):
    cart = request.session.get('cart')
    tax = sum(i['tax'] for i in cart.values() if i)
    delivery_charge = sum(i['delivery_charge'] for i in cart.values() if i)
    
    tax_and_delivery = (tax + delivery_charge)
    
    context = {
        'tax_and_delivery':tax_and_delivery,
    }
    return render(request, 'commerce/checkout.html', context)

def register_v(request):
    if request.user.is_authenticated:
        messages.success(request, f'You already have an account!')
        return redirect('home')
    else:
        if request.method == 'POST':
            form = VendorCreationForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                messages.success(request, f'Your account has been created!')
                return redirect(reverse('admin:index'))
        else:
            form = VendorCreationForm()
    return render(request, 'commerce/vendors/register-v.html', {'form':form})

@login_required(login_url = '/login-vendor/')
def profile_v(request):
    if request.method == 'POST':
        u_form = VendorChangeForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('home')
    else:
        u_form = VendorChangeForm(instance=request.user) 
    
    context = {
        'u_form' : u_form,
    }
    return render(request, 'commerce/vendors/profile.html', context)

@login_required(login_url="/login/")
def orders(request):
    if request.method == "POST":
        address = request.POST.get('address')
        pincode = request.POST.get('pincode')
        mobile = request.POST.get('mobile')
        cart = request.session.get('cart')
        uid = request.session.get('_auth_user_id')
        user = User.objects.get(pk = uid)
        for i in cart:
            a = (int(cart[i]['price']))
            b = cart[i]['quantity']
            total = a*b
            
            order = Order(
                user = user,
                product = cart[i]['product_name'],
                quantity = cart[i]['quantity'],
                price = cart[i]['price'],
                featured_image = cart[i]['featured_image'],
                address = address,
                pincode = pincode,
                mobile = mobile,
                total = total,
            )
            order.save()
        request.session['cart'] = {}
        return redirect("home")
        
    return render(request, '#')

@login_required(login_url="/login/")
def yourorders(request):
    uid = request.session.get('_auth_user_id')
    user = User.objects.get(pk = uid)
    
    order = Order.objects.filter(user = user)
    
    context = {
        'order': order
    }
    return render(request, 'commerce/orders.html', context)

@login_required(login_url="/login/")
def vendor_orders(request):
    vendor = request.user.vendor
    ordered_products = Order.objects.filter(user__vendor__business_name=vendor.business_name).values('product')

    product_ids = [item['product'] for item in ordered_products]
    ordered_products = Product.objects.filter(id__in=product_ids)

    context = {
        'ordered_products': ordered_products
    }

    return render(request, 'commerce/vendors/vendor_orders.html', context)