from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.CreateUserView.as_view(), name="regiser_user"),    #-> User Register path
    path('verify_otp/', views.OtpVerification.as_view(), name="otpverification"),   #-> User otp verification path
    path('resend_otp/', views.ResendOtp.as_view(), name="resendotp"),   #-> Resend OTP path
    path('user_login/', views.UserLoginView.as_view(), name="login_user"),    #-> User login path
    path('admin_login/', views.AdminLoginView.as_view(), name="login_admin"),  #-> Admin login path
    path('user_list/', views.UserListView.as_view(), name="user_list"), #-> user list path
    path('block_unblock_user/', views.BlockUnBlockView.as_view(), name="block_unblock_user"), #-> user block unblock path
    path('profile/', views.UserProfileData.as_view(), name="profile"), #-> user profile data path
    path('userprofileupdate/', views.UserUpdateView.as_view(), name="user_profile_update"), #-> user profile update path
    path('user_google/', views.GoogleLoginView.as_view(), name="google_login"), #-> google login path
    path('forgotemail/', views.UserForgotView.as_view(), name="forgotemail"), #-> User forgot email path
    path('change_password/', views.ChangePassword.as_view(), name="change_password"), #-> User change password path
    path('follow/', views.UserFollow.as_view(), name="follow"), #-> Follow user path
    path('search/', views.SearchUser.as_view(), name="search"), #-> Search User
    path('friends/', views.GetFriends.as_view(), name="friends"), #-> Get all followers and followings
    path('refresh_token/', views.CreateAccessToken.as_view(), name="refresh_token"), #-> Create new access token
]
