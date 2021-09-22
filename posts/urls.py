from django.urls import path

from posts.views import PostDetailView, PostListView

urlpatterns = [
    path('', PostListView.as_view(), name='index'),
    path('post/<slug:slug>/', PostDetailView.as_view(),
         name='post_detail'),
    ]
