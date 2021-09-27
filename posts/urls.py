from django.urls import path

from posts.views import PostDetailView, PostListView, PostCreateView

urlpatterns = [
    path('', PostListView.as_view(), name='index'),
    path('post/add/', PostCreateView.as_view(), name='post_add'),
    path('post/<slug:slug>/', PostDetailView.as_view(),
         name='post_detail'),

    ]
