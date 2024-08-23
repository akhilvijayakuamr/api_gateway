from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.CreateUserView.as_view(), name="regiser_user"),    #-> User Register path
    path('verify_otp/', views.OtpVerification.as_view(), name="otpverification"),   #-> User otp verification path
    path('login/', views.LoginView.as_view(), name="login_user")    #-> User login path
]
