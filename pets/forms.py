from django import forms
from django.forms import inlineformset_factory, BaseInlineFormSet

from pets.models import Pet, ImagePet


class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ('name', 'age', 'weight', 'species', 'breed', 'description',)
        help_texts = {
            'name': 'Имя питомца',
            'age': 'Возраст питомца',
            'weight': 'Вес питомца',
            'species': 'Разновидность: собаки, кошки и т.д.',
            'breed': 'Порода питомца',
            'description': 'Описание питомца',
        }


class ImagePetForm(forms.ModelForm):
    class Meta:
        model = ImagePet
        fields = ('image_name', 'pet', 'image',)
        help_texts = {
            'image_name': 'Название фотогафии',
            'pet': 'Питомец',
            'image': 'Фото',
        }


ImagePetFormSet = inlineformset_factory(Pet, ImagePet,
                                        form=ImagePetForm, extra=2)
