from django.contrib import admin
from . models import (
    Products,
    Customer,
    Cart,
    OrderPlaced
)


# Register your models here.
@admin.register(Products)
class ProductsModelAdmin(admin.ModelAdmin):
    list_display = [ 'id','title', 'initial_price','discounted_price','discription','brand' ,'category','product_image' ]

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display =['id', 'user', 'name', 'division','district','thana','villorroad','zipcode']

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user','product','quantity']

@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'customer','product','quantity','ordered_date','status']