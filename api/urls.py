from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import PetViewSet, UserCodeViewSet, UserTokenViewSet

router = DefaultRouter()
router.register(r'pets', PetViewSet, basename='pets')


auth_urlpatterns = [
    path('email/', UserCodeViewSet.as_view()),
    path('token/', UserTokenViewSet.as_view()),
]


urlpatterns = [
    path('v1/auth/', include(auth_urlpatterns)),
    path('v1/', include(router.urls)),
]
