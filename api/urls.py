from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import PetViewSet

router = DefaultRouter()
router.register(r'pets', PetViewSet, basename='pets')


urlpatterns = [
    path('v1/', include(router.urls)),
]
