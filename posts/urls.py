from django.urls import include, path

from posts.views import (MyPostListView, PostCreateView, PostDetailView,
                         PostListView)

posts_urls = [
    path('add/', PostCreateView.as_view(), name='post_add'),
    path('my_posts/', MyPostListView.as_view(), name='my_posts'),
    path('<slug:slug>/', PostDetailView.as_view(),
         name='post_detail'),
]

urlpatterns = [
    path('', PostListView.as_view(), name='index'),
    path('posts/', include(posts_urls)),
    ]
