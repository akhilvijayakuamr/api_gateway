from django.urls import path
from . import views

urlpatterns = [
    path('create_post/', views.CreatePost.as_view(), name="create_post"), #-> Create post path
    path('post_list/', views.GetAllPost.as_view(), name="post_list"), #-> Get all post path
    path('get_post/', views.GetUniquePost.as_view(), name="get_post"), #-> Get post path
    path('like/', views.LikeApiView.as_view(), name="like_post"), #-> Like post path
    path('comment/', views.CommentApiView.as_view(), name="comment_post"), #-> Comment post path
    path('comment_replay/', views.CommentReply.as_view(), name="comment_replay"), #-> Comment replay path
    path('userpostupdate/', views.UpdatePost.as_view(), name="post_update"), # Update post path
    path('delete_comment/', views.DeleteComment.as_view(), name="delete_comment"), # Delete comment path 
    path('delete_reply/', views.DeleteReply.as_view(), name="delete_reply"), # Delete reply path
    path('post_delete/', views.DeletePost.as_view(), name="post_delete"), # Delete post path
    path('post_report/', views.ReportPost.as_view(), name='post_report'), # Report post path
    path('admin_post_list/', views.GetAdminAllPost.as_view(), name="admin_post_list"), #-> Get all post path
    path('post_hide/', views.HidePost.as_view(), name="post_hide"), # Hide post path
]
