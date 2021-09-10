from django.db import models
from users.models import User


class Species(models.Model):
    name = models.CharField(max_length=30, verbose_name='Название')
    slug = models.SlugField(max_length=30, unique=True, verbose_name='url')

    class Meta:
        verbose_name = 'Разновидность домашнего животного'
        verbose_name_plural = 'Разновидности домашних животных'

    def __str__(self):
        return self.name


class Breed(models.Model):
    name = models.CharField(max_length=30, verbose_name='Название')
    slug = models.SlugField(max_length=30, unique=True, verbose_name='url')
    species = models.ForeignKey(Species, on_delete=models.SET_NULL,
                                blank=True, null=True,
                                verbose_name='Разновидность',
                                related_name='breed')

    class Meta:
        verbose_name = 'Порода'
        verbose_name_plural = 'Породы'

    def __str__(self):
        return self.name


class Pet(models.Model):
    name = models.TextField(max_length=30, verbose_name='Кличка')
    age = models.PositiveSmallIntegerField(db_index=True,
                                           verbose_name='Возраст')
    weight = models.DecimalField(blank=True, max_digits=5, decimal_places=2)
    species = models.ForeignKey(Species, on_delete=models.SET_NULL,
                                blank=True, null=True,
                                verbose_name='Разновидность',
                                related_name='pets')
    breed = models.ForeignKey(Breed, on_delete=models.SET_NULL,
                              blank=True, null=True,
                              verbose_name='Порода',
                              related_name='pets')
    description = models.TextField(blank=True, null=True,
                                   verbose_name='Описание')
    master = models.ForeignKey(User, on_delete=models.CASCADE, blank=True,
                               verbose_name='Владелец',
                               related_name='pets')

    class Meta:
        verbose_name = 'Питомец'
        verbose_name_plural = 'Питомец'

    def __str__(self):
        return self.name


class Tag(models.Model):
    """
    Stores a single Tag entry.
    """
    title = models.CharField('Имя тега', max_length=50, db_index=True)
    display_name = models.CharField('Имя тега для шаблона', max_length=50)

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'теги'

    def __str__(self):
        return self.title
