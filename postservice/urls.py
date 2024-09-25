from django.urls import path
from . import views

urlpatterns = [
    path('create_post/', views.CreatePost.as_view(), name="create_post"), #-> Create post
    path('post_list/', views.GetAllPost.as_view(), name="post_list"), #-> Get all post
    path('get_post/', views.GetUniquePost.as_view(), name="get_post"), #-> Get post
    path('like/', views.LikeApiView.as_view(), name="like_post"), #-> Like post
    path('comment/', views.CommentApiView.as_view(), name="comment_post"), #-> Comment post
    path('comment_replay/', views.CommentReply.as_view(), name="comment_replay"), #-> Comment replay
]
