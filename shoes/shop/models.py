from django.db import models
from django.contrib.auth.models import User

# Create your models here.
CATEGORY_CHOICES = (
    ('women', 'women'),
    ('men', 'men'),    
)

BRAND_CHOICES=(
   
       ('Nike', 'Nike'),
       ('Adidas', 'Adidas'),
       ('Merrel', 'Merrel'),
       ('Gucci', 'Gucci'),
       ('Skechers' , 'Skechers'),   
)

COLORS_CHOICES=(
    ('Black' , 'Black'),
    ('White', 'White'),
    ('Blue', 'Blue'),
    ('Red', 'Red'),
    ('Green', 'Green'),
    ('Grey', 'Grey'),
    ('Orange', 'Orange'),
    ('Cream', 'Cream'),
    ('Brown', 'Brown'), 
)

TECHNOLOGIES_CHOICES=(

    ('BioBevel', 'BioBevel'),
    ( 'Groove', 'Groove'),
    ('FlexBevel', 'FlexBevel'),
)

MATERICAL_CHOICES=(
    ('Leather', 'Leather'),
    ('Suede', 'Suedue'),
)

STYLE_CHOICES=(
    ('Oxfords','Oxfords'),
    ('Lace_Ups', 'Lace_Ups'),
    ('Sandals','Sandals'),
    ('Boots', 'Boots'),
    ( 'Slip_Ons', 'Slip_Ons'),
)



WIDTH_CHOICES=(
    ('M', 'M'),
    ('W','W'),
)


class Products(models.Model):
    title= models.CharField(max_length=100)
    initial_price= models.FloatField()
    discounted_price= models.FloatField()
    discription=models.CharField(max_length=200 )
    brand= models.CharField(choices=BRAND_CHOICES, max_length=10)
    category= models.CharField(choices=CATEGORY_CHOICES,max_length=5)
    product_image= models.ImageField(upload_to='product_image')
    Colors =models.CharField(choices=COLORS_CHOICES, max_length=10)
    Technologies=models.CharField(choices=TECHNOLOGIES_CHOICES, max_length=10)
    Material=models.CharField(choices=MATERICAL_CHOICES, max_length=10)
    Style=models.CharField(choices=STYLE_CHOICES, max_length=10)
    Size=models.FloatField()
    Width=models.CharField(choices=WIDTH_CHOICES, max_length=1)

    def __str__(self):
        return str(self.id)

DIVISION_CHOICES = (
    ('Dhaka','Dhaka'),
    ('Rangpur','Rangpur'),
    ('Rajshahi','Rajshahi'),
    ('Khulna','Khulna'),
    ('Barishal','Barishal'),
    ('Chattogram','Chattogram'),
    ('Mymenshing','Mymenshing'),
    ('Sylhet','Sylhet'),
)

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    division = models.CharField(choices=DIVISION_CHOICES, max_length=50)
    district = models.CharField(max_length=200)
    thana = models.CharField(max_length=50)
    villorroad = models.CharField(max_length=50)
    zipcode = models.IntegerField()
    

    def __str__(self):
        return str(self.id)
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)
    
    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price



STATUS_CHOICE = (
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On the Way', 'On the Way'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel')
)

class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICE, default='Pending')

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price
