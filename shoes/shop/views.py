from django.shortcuts import render,redirect,get_object_or_404
from . models import Products,Customer,Cart,OrderPlaced
from . forms import CustomerRegistrationForm, LoginForm, CustomerProfileForm
from django.contrib import messages
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Q



# Create your views here.

def home(request):
    products= Products.objects.all() # get all products
    total_item=0
    if request.user.is_authenticated:
       total_item = len(Cart.objects.filter(user=request.user))
    return render(request, 'shop/index.html', {'products':products, 'total_item':total_item })

def produtcdetatils(request , product_id):
    total_item= 0
    particular_product=Products.objects.get(id=product_id)
    item_already_in_cart = False
    if request.user.is_authenticated:
        total_item = len(Cart.objects.filter(user=request.user))
        item_already_in_cart = Cart.objects.filter(Q(product=particular_product.id) & Q(user=request.user)).exists()       
    return render(request, 'shop/product-detail.html', {'particular_product':particular_product, 'item_already_in_cart':item_already_in_cart, 'total_item':total_item} )

def menproduct(request):
    men_shoes= Products.objects.filter(category='men')
    total_item=0
    if request.user.is_authenticated:
       total_item = len(Cart.objects.filter(user=request.user))
    return render(request, 'shop/men.html', {'men_shoes':men_shoes,'total_item':total_item})

def womenproduct(request, data=None):
    brand=['Nike', 'Adidas', 'Merrel', 'Gucci', 'Skechers']
    colors=['Black','White', 'Red', 'Green ', 'Grey', 'Blue','Orange', 'Cream','Brown']
    
    if data in brand:
        women_shoes=Products.objects.filter(category='women').filter(brand=data)
    elif data in colors:
        women_shoes=Products.objects.filter(category='women').filter(Colors=data)    
    else:
        women_shoes=Products.objects.filter(category = 'women')         
    total_item=0
    if request.user.is_authenticated:
       total_item = len(Cart.objects.filter(user=request.user))       
    return render(request, 'shop/women.html' , {'women_shoes': women_shoes, 'total_item':total_item})


def about(request):
    total_item=0
    if request.user.is_authenticated:
       total_item = len(Cart.objects.filter(user=request.user))
    return render(request, 'shop/about.html',{ 'total_item':total_item})


@method_decorator(login_required, name='dispatch')
class Profile_View(View):
    def get(self, request):      
        form = CustomerProfileForm()
        total_item=0
        if request.user.is_authenticated:
         total_item = len(Cart.objects.filter(user=request.user))
        return render(request, 'shop/profile.html', {'form':form, 'active':'btn-primary',  'total_item':total_item})
    def post(self, request):
        if request.method =='POST':
            form = CustomerProfileForm(request.POST)
            if form.is_valid():
                usr = request.user
                name = form.cleaned_data['name']
                division = form.cleaned_data['division']
                district = form.cleaned_data['district']
                thana = form.cleaned_data['thana']
                villorroad = form.cleaned_data['villorroad']
                zipcode = form.cleaned_data['zipcode']
                reg = Customer(user=usr,name=name, division=division,district=district, thana=thana, villorroad=villorroad, zipcode=zipcode)
                reg.save()
                messages.success(request, 'Congratulations! Profile Updated Successfully') 
                form=CustomerProfileForm() 
            total_item=0
            if request.user.is_authenticated:
                total_item = len(Cart.objects.filter(user=request.user))       
            return render(request, 'shop/profile.html', {'form':form, 'active':'btn-primary', 'total_item':total_item})
        

@login_required
def address(request):
    add = Customer.objects.filter(user=request.user)
    total_item=0
    if request.user.is_authenticated:
        total_item = len(Cart.objects.filter(user=request.user))
    return render(request, 'shop/address.html', {'add':add, 'active':'btn-primary', 'total_item':total_item})



@login_required
def Add_to_cart(request):
    user=request.user
    product_id=request.GET.get('prod_id')
    product= Products.objects.get(id=product_id)
    Cart(user=user, product=product).save()    
    return redirect('/cart')

def show_cart(request):
    total_item= 0
    if request.user.is_authenticated:
        user = request.user
        cart_items = Cart.objects.filter(user=user)
        total_item = len(Cart.objects.filter(user=request.user))
        
        amount = 0.0
        shipping_amount = 100.0   
        count=0
        discounted_price=30
        if cart_items:
            for item in cart_items:
                item_total = item.quantity * item.product.discounted_price            
                amount += item_total
            
            total_amount = amount + shipping_amount + discounted_price # Remove extra flat discount unless needed

            context = {
                'carts': cart_items,
                'amount': amount,
                'totalamount': total_amount,
                'shipping_amount': shipping_amount,  
                'discounted_price': discounted_price,
                'total_item':total_item,      
            }
    
        else:
            return render(request, 'shop/emptycart.html')
    
    return render(request, 'shop/cart.html', context)


def update_quantity(request):
    if request.method == 'POST':
        for cart in Cart.objects.filter(user=request.user):
            new_qty = request.POST.get(f'quantity_{cart.id}')
            if new_qty:
                cart.quantity = int(new_qty)
                cart.save()
        return redirect('/cart')  #  Redirecting back to the cart instead of add_to_cart


def remove_cart_item(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    cart_item.delete()
    return redirect('/cart')


@login_required
def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 100.0
    totalamount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
            totalamount = amount+ shipping_amount
    total_item=0
    if request.user.is_authenticated:
       total_item = len(Cart.objects.filter(user=request.user))
    return render(request, 'shop/checkout.html', {'add':add, 'totalamount':totalamount, 'cart_items':cart_items,'shipping_amount':shipping_amount,  'total_item':total_item})

@login_required
def order(request):
    op = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'shop/order-complete.html', {'order_placed':op})

@login_required
def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    if custid:
        customer = Customer.objects.get(id=custid)
        cart = Cart.objects.filter(user=user)
        for c in cart:
            OrderPlaced(user=user, customer=customer, product = c.product, quantity=c.quantity).save()
            c.delete()
        return redirect('/order')
    else:
        messages.error(request, "Please select a shipping address before continuing.")
        return redirect('/checkout')


def contact(request):
    total_item=0
    if request.user.is_authenticated:
       total_item = len(Cart.objects.filter(user=request.user))
    return render(request, 'shop/contact.html',{ 'total_item':total_item})



class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'shop/customerregistration.html', {'form':form})
    
    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulations, registration done')
            form.save()
        return render(request, 'shop/customerregistration.html', {'form':form})