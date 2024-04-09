from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
import datetime 

class Category(models.Model):
    cate_name_eng = models.CharField(max_length=50, default='')
    cate_name_ru = models.CharField(max_length=50, default='')
    
    @staticmethod
    def get_all_categories(): 
        return Category.objects.all() 
  
    def __str__(self): 
        return self.cate_name_eng


class Product(models.Model):
    product_name_eng = models.CharField(max_length=255, default='')
    product_name_ru = models.CharField(max_length=255, default='')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    color = models.CharField(max_length=7, default='')
    size = models.CharField(max_length=10, default='')
    image = models.ImageField(upload_to='product_images/')
    image_hover = models.ImageField(upload_to='product_images/', blank=True)
    image_detail1 = models.ImageField(upload_to='product_images/', blank=True)
    image_detail2 = models.ImageField(upload_to='product_images/', blank=True)
  
    @staticmethod
    def get_products_by_id(ids): 
        return Product.objects.filter(id__in=ids) 
  
    @staticmethod
    def get_all_products(): 
        return Product.objects.all() 
  
    @staticmethod
    def get_all_products_by_categoryid(category_id): 
        if category_id: 
            return Product.objects.filter(category=category_id) 
        else: 
            return Product.get_all_products()


class Customer(models.Model): 
    first_name = models.CharField(max_length=50) 
    last_name = models.CharField(max_length=50) 
    phone = models.CharField(max_length=10) 
    email = models.EmailField() 
    address = models.CharField(max_length=50, default='', blank=True) 
    
    def register(self): 
        self.save() 
  
    @staticmethod
    def get_customer_by_email(email): 
        try: 
            return Customer.objects.get(email=email) 
        except: 
            return False
  
    def isExists(self): 
        if Customer.objects.filter(email=self.email): 
            return True
  
        return False


class Order(models.Model): 
    id_order = models.AutoField(primary_key=True, default=0)
    product = models.ForeignKey(Product, 
                                on_delete=models.CASCADE, default=None) 
    quantity = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    customer = models.ForeignKey(Customer, 
                                 on_delete=models.CASCADE) 

    

    def final_price(self):
        final_price = (self.product.price - self.product.discount) * self.quatity
        return final_price

    def customer_address(self):
        return self.customer.address
    
    def customer_phone(self):
        return self.customer.phone

