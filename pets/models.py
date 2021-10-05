from django.db import models
from django.template.defaultfilters import slugify
from unidecode import unidecode

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
    slug = models.SlugField(unique=True)
    age = models.PositiveSmallIntegerField(db_index=True,
                                           verbose_name='Возраст')
    weight = models.DecimalField(blank=True, max_digits=5, decimal_places=2,
                                 verbose_name='Вес')
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
    date_adding = models.DateTimeField(auto_now=True)

    def save(self):
        if not self.id:  # if this is a new item
            new_slug = '{0}-{1}-{2}'.format(self.name, self.master,
                                            self.date_adding)
            self.slug = slugify(unidecode(new_slug))
        super(Pet, self).save()

    class Meta:
        verbose_name = 'Питомец'
        verbose_name_plural = 'Питомцы'
        ordering = ["-date_adding"]

    def __str__(self):
        return self.name


class ImagePet(models.Model):
    image_name = models.TextField(max_length=30, blank=True, default='image',
                                  verbose_name='Название фотографии')
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, blank=True,
                            verbose_name='Фото питомца',
                            related_name='images')
    image = models.ImageField('Изображение', upload_to='pet_images/',
                              blank=True, null=True)

    class Meta:
        verbose_name = 'Фотография питомца'
        verbose_name_plural = 'Фотографии питомца'
