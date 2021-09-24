from django import forms
from django.forms.models import inlineformset_factory

from pets.models import Pet
from posts.models import Comment, Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('group', 'text',)
        help_texts = {
            'group': 'Выберите группу для размещения вашего поста',
            'text': 'Текст вашего поста',
            'image': 'Изображение для вашего поста',
        }


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


PostFormset = inlineformset_factory(Pet, Post, PostForm)


class CommentForm(forms.ModelForm):
    """ Форма для создания комментария """
    class Meta:
        model = Comment
        fields = ('text',)
        help_texts = {'text': 'Текст вашего комментария к посту'}
