from django.urls import path

from pets.views import PetAddView

urlpatterns = [
    path('add/', PetAddView.as_view(), name='pet_add'),
    ]
