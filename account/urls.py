from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.user_view, name='users'),
    path('users/reset_password', views.reset_password, name='reset password'),
    path('users/create', views.create_account, name='create users'),
    path('auth', views.login_view, name='login'),
    path('auth/forgot_password', views.forgot_password, name="forgot password"),
    path('auth/verify_otp_forgot_password', views.verify_otp_pass, name="verify otp change pass"),
    path('users/profile/', views.profile_view, name='profile'),
    path('users/verify_otp/', views.verify_otp),
    path('users/new_otp/', views.new_otp),
    
]