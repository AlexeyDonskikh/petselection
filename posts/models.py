from django.db import models
from django.template.defaultfilters import slugify
from unidecode import unidecode

from pets.models import Pet
from users.models import User


class Group(models.Model):
    title = models.CharField(max_length=200, db_index=True,
                             verbose_name='Название группы')
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, db_index=True,
                                   verbose_name='Описание группы')

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def __str__(self):
        return self.title


class Post(models.Model):
    title = models.CharField(max_length=200, db_index=True,
                             verbose_name='Заголовок поста')
    pet = models.ForeignKey(Pet, blank=False, on_delete=models.CASCADE,
                            verbose_name='Питомец', related_name='pet')
    slug = models.SlugField(unique=True)
    text = models.TextField(verbose_name='Текст поста')
    pub_date = models.DateTimeField("Дата публикации",
                                    auto_now_add=True,
                                    db_index=True)
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name="posts",
                               verbose_name='Автор поста')
    group = models.ForeignKey(Group,
                              on_delete=models.SET_NULL,
                              blank=True, null=True,
                              related_name="posts",
                              verbose_name='Группа')

    def save(self):
        if not self.id:
            new_slug = '{0}-{1}-{2}'.format(self.title, self.author,
                                            self.pub_date)
            self.slug = slugify(unidecode(new_slug))
        if not self.title:
            self.title = self.pet.name
        super(Post, self).save()

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ["-pub_date"]


class Comment(models.Model):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             blank=True,
                             null=True,
                             related_name="comments",
                             verbose_name='Поста')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name="comments",
                               verbose_name='Автор комментария')
    text = models.TextField(max_length=500, verbose_name='Текст комментария')
    created = models.DateTimeField("Дата создания комментария",
                                   auto_now_add=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Коментарии'


class Follow(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name="follower",
                             verbose_name='Подписчик')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name="following",
                               verbose_name='Автор')

    class Meta:
        unique_together = (("user", "author"),)
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
