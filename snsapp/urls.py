from django.urls import path
from .views import Home, MyPost, DetailPost, CreatePost, UpdatePost, DeletePost, LikeBase, FollowBase, FollowList
              #Home, MyPost追加


urlpatterns = [
   path('', Home.as_view(), name='home'),             #追加
   path('mypost/', MyPost.as_view(), name='mypost'),  #追加
   path('post/<int:pk>', DetailPost.as_view(), name='detail'), #追加
   path('post/<int:pk>/update', UpdatePost.as_view(), name='update'), #追加
   path('post/<int:pk>/delete', DeletePost.as_view(), name='delete'), #追加
   path('create/', CreatePost.as_view(), name='create'),      #追加
   path('like/<int:pk>/', LikeBase.as_view(), name='like'),
   path('users/<int:pk>/follow/', FollowBase.as_view(), name='follow'),
   path('follow-list/', FollowList.as_view(), name='follow-list'),
]