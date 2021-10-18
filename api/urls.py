from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (CommentViewSet, GroupViewSet, PetViewSet, PostViewSet,
                       UserCodeViewSet, UserTokenViewSet, UserViewSet)

router = DefaultRouter()
router.register(r'groups', GroupViewSet, basename='groups')
router.register(r'pets', PetViewSet, basename='pets')
router.register(r'users', UserViewSet, basename='users')
router.register(
    r'posts/(?P<post_id>[\d]+)/comments',
    CommentViewSet, basename='comments'
)
router.register(r'posts', PostViewSet, basename='posts')


auth_urlpatterns = [
    path('email/', UserCodeViewSet.as_view()),
    path('token/', UserTokenViewSet.as_view()),
]


urlpatterns = [
    path('v1/auth/', include(auth_urlpatterns)),
    path('v1/', include(router.urls)),
]
