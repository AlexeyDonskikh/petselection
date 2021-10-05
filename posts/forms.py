from django import forms

from posts.models import Comment, Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'pet', 'group', 'text',)
        help_texts = {
            'title': 'Заголовок поста',
            'pet': 'Выберите питомца для добавления в пост',
            'group': 'Выберите группу для размещения вашего поста',
            'text': 'Текст вашего поста',
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        help_texts = {'text': 'Текст вашего комментария к посту'}
