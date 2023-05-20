from django.urls import path
from . import views 
from .views import add_money, wallet, orders, yourorders, vendor_orders
from django.conf import settings 
from django.conf.urls.static import static
from commerce import views as commerce_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register-vendor/', commerce_views.register_v, name='register_vendor'),
    path('login-vendor/', auth_views.LoginView.as_view(template_name='commerce/vendors/login-v.html'), name='login_vendor'),
    path('404', views.Error404, name='404'),
    path('base/', views.BASE, name='base'),
    path('about/', views.about, name='about'),
    path('', views.HOME, name='home'),
    path('contact/', views.contact, name='contact'),
    path('add-money/', add_money, name='add_money'),
    path('wallet/', wallet, name='wallet'),
    path('product/', views.product, name='product'),
    path('submit-review/<slug:slug>', views.submit_review, name='submit_review'),
    path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/',
         views.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/',
         views.item_decrement, name='item_decrement'),
    path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
    path('cart/cart-detail/',views.cart_detail,name='cart_detail'),
    path('product/filter-data',views.filter_data,name="filter-data"),
    path('product/<slug:slug>', views.PRODUCT_DETAILS,name='product_detail'),
    path('checkout/', views.checkout,name='checkout'),
    path('filter_data/', views.filter_data, name='filter_data'),
    path('orders/', views.orders, name='orders'),
    path('yourorders/', views.yourorders, name='yourorders'),
    path('vendor/orders/', views.vendor_orders, name='vendor_orders'),
] +static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
