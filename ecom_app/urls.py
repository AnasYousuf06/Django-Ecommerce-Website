from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_view
from . form import LoginForm,  MyPasswordResetForm ,MyPasswordChangeForm, MySetPasswordForm
urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('category/<slug:val>', views.CategoryView.as_view(),name="category"),
    path('category-title/<val>', views.CategoryView.as_view(),name="category-title"),
    path('product/<int:pk>', views.ProductDetail.as_view(),name="product"),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('addtocart/', views.add_to_cart, name='addtocart'),
    path('cart/', views.show_cart, name='showcart'),
    path('checkout/', views.Checkout.as_view(), name='checkout'),
    path('pluscart/', views.plus_cart),
    path('minuscart/', views.minus_cart),
    path('removecart/', views.remove_cart),
    path('paymentdone/', views.payment_done, name='paymentdone'),
    path('orders/', views.home , name='orders'),

    path('login/',auth_view.LoginView.as_view(template_name= 'app/login.html',authentication_form=LoginForm),name='login'),
    path('logout/', auth_view.LogoutView.as_view(next_page='login'), name='logout'),
    path('registration/',views.CustomerRegistrationView.as_view(),name='registration'),
    
    path('password-change/',auth_view.PasswordChangeView.as_view(template_name='app/changepassword.html',form_class=MyPasswordChangeForm,success_url='/passwordchangedone'), name = 'passwordchange'),
    path('passwordchangedone/',auth_view.PasswordChangeDoneView.as_view(template_name='app/passwordchangedone.html'), name = 'passwordchangedone'),
    path('updateaddress/<int:pk>/', views.UpdateAddress.as_view(),name = 'updateaddress'),
    
    path('password-reset/',auth_view.PasswordResetView.as_view(template_name= 'app/password_reset.html',form_class= MyPasswordResetForm),name='password_reset'),

    path('password-reset/done/',auth_view.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html') , name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html',form_class=MySetPasswordForm) , name='password_reset_confirm'),

    path('password-reset-complete/', auth_view.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'), name='password_reset_complete'),
    





] 