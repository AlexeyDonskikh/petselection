from django.urls import path


from pets.views import PetListView


urlpatterns = [
    path('', PetListView.as_view(), name='index'),
    ]
