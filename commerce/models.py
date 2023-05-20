from django.db import models
from ckeditor.fields import RichTextField 
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django_currentuser.middleware import get_current_user
import datetime
from django.contrib.auth import get_user_model

User = get_user_model()


class Vendor(User):
    business_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    address = models.TextField()
    
    def save(self, *args, **kwargs):
        self.is_staff = True
        super(Vendor, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.business_name

class slider(models.Model):
    DISCOUNT_DEAL = (
        ('NEW ARRIVALS', 'NEW ARRIVALS'),
        ('FESTIVE OFFERS', 'FESTIVE OFFERS'),
        ('SEASONAL DEALS', 'SEASONAL DEALS'),
        ('HYPE', 'HYPE'),
    )
    
    
    Image = models.ImageField(upload_to= 'media/slider_imgs')
    Discount_Deal = models. CharField(choices=DISCOUNT_DEAL,max_length=100)
    Sale = models.IntegerField()
    Brand_Name = models.CharField(max_length=200)
    Discount = models.IntegerField()
    Link = models.CharField(max_length=200)
    
    def __str__(self):
        return self.Brand_Name
    
class Main_Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Category(models.Model):
    main_category = models.ForeignKey(Main_Category,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)


    def __str__(self):
        return self.name + " -- " + self.main_category.name

class Sub_Category(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.category.main_category.name + " -- " + self.category.name + " -- " + self.name

class Section(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Color(models.Model):
    code = models.CharField(max_length=100)
    
    def __str__(self):
        return self.code   
    
class Brand(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name 

class Product(models.Model):
    total_quantity = models.IntegerField()
    Availability = models.IntegerField()
    featured_image = models.CharField(max_length=100)
    product_name = models.CharField(max_length=100)
    Brand = models.ForeignKey(Brand,on_delete=models.CASCADE, null=True)
    price = models.IntegerField()
    Discount = models.IntegerField()
    tax = models.IntegerField(null=True)
    delivery_charge = models.IntegerField(null=True)
    Product_information = RichTextField(null=True)
    model_Name = models.CharField(max_length=100)
    Categories = models.ForeignKey(Category,on_delete=models.CASCADE)
    color = models.ForeignKey(Color,on_delete=models.CASCADE, null=True)
    Tags = models.CharField(max_length=100)
    Description = RichTextField()
    section = models.ForeignKey(Section,on_delete=models.DO_NOTHING)
    slug = models.SlugField(default='', max_length=500, null=True, blank=True)
    
    def __str__(self):
        return self.product_name
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("product_detail", kwargs={'slug': self.slug})

    class Meta:
        db_table = "commerce.apps.CommerceConfig_Product"
    
        
class VendorManager(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.product.product_name
    

def create_slug(instance, new_slug=None):
    slug = slugify(instance.product_name)
    if new_slug is not None:
        slug = new_slug
    qs = Product.objects.filter(slug=slug).order_by('-id')
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug

def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, Product)

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    comment = models.TextField()
    name = models.CharField(max_length=255)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

class Product_Image(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    Image_url = models.CharField(max_length=200)

class Additional_Information(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    specification = models.CharField(max_length=100)
    detail = models.CharField(max_length=100)
    
class Order(models.Model):
    featured_image = models.ImageField(upload_to='media/image')
    product = models.CharField(max_length=1000, default='')
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    quantity = models.CharField(max_length=5)
    price = models.IntegerField()
    total = models.CharField(max_length=1000, default='')
    address = models.TextField()
    mobile = models.CharField(max_length=10)
    pincode = models.CharField(max_length=10)
    date = models.DateTimeField(default=datetime.datetime.today)
    
    def __str__(self):
        return self.product

    def save(self, *args, **kwargs):
        # Decrease the availability of the product
        try:
            product = Product.objects.get(product_name=self.product)
            product.Availability -= int(self.quantity)
            product.save()
        except Product.DoesNotExist:
            pass

        super().save(*args, **kwargs)