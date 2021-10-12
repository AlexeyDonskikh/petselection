from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from pets.models import ImagePet, Pet


class PetSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'species', 'breed', 'age', 'weight', 'master',
                  'description',)
        model = Pet
