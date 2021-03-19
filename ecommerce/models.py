from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class MainBuyer(models.Model):
    name = models.CharField(max_length=128, null=True, blank=True)    
    email = models.EmailField(max_length=64, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=128, null=True, blank=True)    
    mainbuyer = models.ForeignKey(MainBuyer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    title = models.CharField(max_length=128, null=True, blank=True)
    digital = models.BooleanField(default=False, null=True, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)    
    description = models.TextField(null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    photo = models.FileField('product_photo', upload_to='photo', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.name

class CompanyInfo(models.Model):    
    account = models.CharField(max_length=128, null=True, blank=True)
    company = models.CharField(max_length=128, null=True, blank=True)
    street_english = models.CharField(max_length=128, null=True, blank=True)
    street_chinese = models.CharField(max_length=128, null=True, blank=True)
    country = models.CharField(max_length=128, null=True, blank=True)
    city = models.CharField(max_length=128, null=True, blank=True)
    postal_code = models.CharField(max_length=128, null=True, blank=True)
    state = models.CharField(max_length=128, null=True, blank=True)
    accounting_attention_person = models.CharField(max_length=128, null=True, blank=True)
    account_email = models.EmailField(max_length=64, null=True, blank=True)    
    purchase_attention_person = models.CharField(max_length=128, null=True, blank=True)
    purchase_email = models.EmailField(max_length=64, null=True, blank=True)
    phone = models.EmailField(max_length=64, null=True, blank=True)
    fax = models.EmailField(max_length=64, null=True, blank=True)
    vat = models.EmailField(max_length=64, null=True, blank=True)
    brands = models.ForeignKey(MainBuyer, on_delete=models.CASCADE)
    is_agent = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return self.account

class CustomerDetail(models.Model):
    company = models.CharField(max_length=128, null=True, blank=True)
    contact_person = models.CharField(max_length=128, null=True, blank=True)
    contact_email = models.EmailField(max_length=64, null=True, blank=True)
    order_number = models.CharField(max_length=64, null=True, blank=True)
    supplier_code = models.CharField(max_length=64, null=True, blank=True)

    def __str__(self):
        return self.supplier_code

class Localbuyer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    status = models.BooleanField(null=True, blank=True)
    name = models.CharField(max_length=128, null=True, blank=True)
    company_info = models.OneToOneField(CompanyInfo, on_delete=models.CASCADE)
    customer_detail = models.OneToOneField(CustomerDetail, on_delete=models.CASCADE)

    def __str__(self):
        return self.status

class DelivaryAddress(models.Model):
    user = models.ForeignKey(Localbuyer, on_delete = models.CASCADE)
    street = models.CharField(max_length=128, null=True, blank=True)
    city = models.CharField(max_length=128, null=True, blank=True)
    zipcode = models.CharField(max_length=128, null=True, blank=True)
    country = models.CharField(max_length=128, null=True, blank=True)

    def __str__(self):
        return self.id

class BillingAddress(models.Model):
    user = models.ForeignKey(Localbuyer, on_delete = models.CASCADE)
    street = models.CharField(max_length=128, null=True, blank=True)
    city = models.CharField(max_length=128, null=True, blank=True)
    zipcode = models.CharField(max_length=128, null=True, blank=True)
    country = models.CharField(max_length=128, null=True, blank=True)

    def __str__(self):
        return self.id

class Order(models.Model):
    customer = models.ForeignKey(Localbuyer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=128, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitems_set.all()

        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        
        return shipping

    @property
    def get_cart_total(self):
        orderitems = self.orderitems_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    
    @property
    def get_cart_items(self):
        orderitems = self.orderitems_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItems(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Localbuyer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state= models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address