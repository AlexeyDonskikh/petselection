from rest_framework import filters, mixins, status, viewsets

from api.serializers import PetSerializer
from pets.models import ImagePet, Pet


class PetViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer
    filter_backends = (filters.SearchFilter, )
    search_fields = ('^name', '^breed', '^master',)
