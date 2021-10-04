from django.urls import path

from pets.views import PetAddView, PetUpdateView, MyPetListView, PetDetailView

urlpatterns = [
    path('my_pets/', MyPetListView.as_view(), name='my_pets'),
    path('my_pets/<slug:slug>/', PetDetailView.as_view(), name='pet_detail'),
    path('add/', PetAddView.as_view(), name='pet_add'),
    path('update/', PetUpdateView.as_view(), name='pet_update'),
    ]
