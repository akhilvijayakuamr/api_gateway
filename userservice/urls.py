from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.CreateUserView.as_view(), name="regiser_user"),    #-> User Register path
    path('verify_otp/', views.OtpVerification.as_view(), name="otpverification"),   #-> User otp verification path
    path('resend_otp/', views.ResendOtp.as_view(), name="resendotp"),   #-> Resend OTP path
    path('user_login/', views.UserLoginView.as_view(), name="login_user"),    #-> User login path
    path('admin_login/', views.AdminLoginView.as_view(), name="login_admin"),  #-> Admin login path
    path('user_list/', views.UserListView.as_view(), name="user_list"), #-> user list path
]
