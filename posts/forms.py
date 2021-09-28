from django import forms
from django.forms.models import inlineformset_factory

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


class CommentForm(forms.ModelForm):
    """ Форма для создания комментария """
    class Meta:
        model = Comment
        fields = ('text',)
        help_texts = {'text': 'Текст вашего комментария к посту'}
