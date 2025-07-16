from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from . forms import LoginForm, MyPasswordChangeForm, MyPasswordResetForm,MySetPasswordForm

urlpatterns = [
    
    path('', views.home, name='home'),
    path('womenproduct/<slug:data>', views.womenproduct, name='womenproduct'),
    path('menproduct/', views.menproduct, name='menproduct'), 
    path('about/', views.about, name='about'),

    path('add_to_cart/', views.Add_to_cart, name='add_to_cart'), 
    path('cart/', views.show_cart, name='show_cart'),
    path('update_quantity/',views.update_quantity, name='update_quantity'),
    path('remove/<int:cart_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('paymentdone/', views.payment_done, name='paymentdone'),
    path('contact/' , views.contact, name='contact'), 
    path('checkout/', views.checkout, name='checkout'),
    path('order/', views.order, name='order'), 
    path('productdetail/<int:product_id>', views.produtcdetatils, name='productdetails'), 
    path('address/', views.address, name='address'),
   
    

# login route
    path('accounts/login/', auth_views.LoginView.as_view(template_name='shop/login.html', authentication_form=LoginForm), name='login'),
    path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),
    path('profile/', views.Profile_View.as_view(), name='profile'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('changepassword/', auth_views.PasswordChangeView.as_view(template_name='shop/passwordchange.html', form_class=MyPasswordChangeForm, success_url='/passwordchangedone/'), name='passwordchange'),
    path('passwordchangedone/', auth_views.PasswordChangeView.as_view(template_name='shop/passwordchangedone.html'), name='passwordchangedone'),
    path('password-reset', auth_views.PasswordResetView.as_view(template_name='shop/password_reset.html', form_class=MyPasswordResetForm), name='password_reset'),
    path('password-reset/done', auth_views.PasswordResetDoneView.as_view(template_name='shop/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='shop/password_reset_confirm.html', form_class=MySetPasswordForm), name='password_reset_confirm'),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='shop/password_reset_complete.html'),name='password_reset_complete'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)