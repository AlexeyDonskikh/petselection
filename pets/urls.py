from django.urls import path

from pets.views import MyPetListView, PetAddView, PetDetailView, PetUpdateView

urlpatterns = [
    path('my_pets/', MyPetListView.as_view(), name='my_pets'),
    path('my_pets/<slug:slug>/', PetDetailView.as_view(), name='pet_detail'),
    path('add/', PetAddView.as_view(), name='pet_add'),
    path('update/<slug:slug>/', PetUpdateView.as_view(), name='pet_update'),
    ]
