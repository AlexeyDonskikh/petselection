from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.text import slugify
from unidecode import unidecode

from users.managers import UserManager


class UserRole(models.TextChoices):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'


class User(AbstractUser):
    username_validator = UnicodeUsernameValidator()
    slug = models.SlugField(unique=True)
    email = models.EmailField(help_text='email address', unique=True)

    role = models.CharField(
        max_length=10, choices=UserRole.choices, default=UserRole.USER)

    bio = models.TextField(max_length=500, blank=True)
    first_name = models.CharField(max_length=50, blank=True,
                                  verbose_name='Имя')
    last_name = models.CharField(max_length=50, blank=True,
                                 verbose_name='Фамилия')
    created = models.DateTimeField("Дата создания аккаунта",
                                   auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def save(self, *args, **kwargs):
        self.slug = slugify(unidecode(self.username))
        super().save(*args, **kwargs)

    @property
    def is_admin(self):
        return self.role == UserRole.ADMIN

    @property
    def is_moderator(self):
        return self.role == UserRole.MODERATOR


class UserCode(models.Model):
    email = models.EmailField(primary_key=True, unique=True)
    confirmation_code = models.CharField(max_length=30)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
