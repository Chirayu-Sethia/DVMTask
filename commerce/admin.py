from django.contrib import admin
from django.urls import reverse
from django.contrib.auth.admin import UserAdmin
from .models import *
from .models import Vendor, Review, Order
from .models import VendorManager
from .forms import VendorCreationForm, VendorChangeForm
from django.contrib.admin import AdminSite
from import_export import resources
from import_export.admin import ExportMixin
from django import forms
from import_export.formats import base_formats
from django.http import HttpResponse
from import_export.admin import ImportExportModelAdmin

class VendorAdmin(UserAdmin):
    add_form = VendorCreationForm
    form = VendorChangeForm
    model = Vendor
    list_display = ('username', 'email', 'business_name', 'phone_number', 'address', 'is_staff')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'business_name', 'phone_number', 'address',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'business_name', 'phone_number', 'address', 'is_staff', 'is_superuser'),
        }),
    )
    search_fields = ('username', 'email', 'business_name', 'phone_number', 'address',)
    ordering = ('username',)

class VendorProductAdmin(admin.ModelAdmin):
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(vendor=request.user.vendor)
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "vendor":
            kwargs["queryset"] = Vendor.objects.filter(business_name=request.user.vendor.business_name)
            kwargs["initial"] = kwargs["queryset"].first()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.vendor = request.user.vendor
        super().save_model(request, obj, form, change)

    def get_readonly_fields(self, request, obj=None):
        if obj and not request.user.is_superuser:
            return ['vendor']
        return []
    
    def get_success_url(self, request):
        return reverse('admin:commerce_vendormanager_changelist')
    
    
class Product_Images(admin.TabularInline):
    model = Product_Image

class Additional_Informations(admin.TabularInline):
    model = Additional_Information

class Product_Admin(admin.ModelAdmin):
    inlines = (Product_Images,Additional_Informations)
    list_display = ('product_name','price', 'Categories','color', 'section')
    list_editable = ('Categories', 'section', 'color')
 
class OrderResource(resources.ModelResource):

    class Meta:
        model = Order
        exclude = ('featured_image',)
        
    def dehydrate_user(self, order):
        user = order.user
        if user:
            return user.username
        return ''
          
class OrderAdmin(ImportExportModelAdmin):
    resource_classes = [OrderResource]
    
# Register the models with the custom ModelAdmin classes
admin.site.register(Vendor, VendorAdmin)
admin.site.register(VendorManager, VendorProductAdmin)
admin.site.register(Section)
admin.site.register(Product, Product_Admin)
admin.site.register(Product_Image)
admin.site.register(Additional_Information)	
admin.site.register(Review)
admin.site.register(slider)
admin.site.register(Main_Category)
admin.site.register(Category)
admin.site.register(Sub_Category)
admin.site.register(Color)
admin.site.register(Brand)
admin.site.register(Order, OrderAdmin)