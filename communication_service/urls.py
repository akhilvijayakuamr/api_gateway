from django.urls import path
from . import views


urlpatterns = [
   path('chat_list/', views.ChatList.as_view(), name="chat_list"),   #-> Get specific user chat
   path('chat_user/', views.ChatUserList.as_view(), name="chat_user_list"),   #-> Get Chat users
   path('get_notification/', views.GetNotifications.as_view(), name="get_notification"), #-> Get all notifications
   path('read_notification/', views.ReadNotification.as_view(), name="read_all_notifications"), #-> Read all notifications
]
