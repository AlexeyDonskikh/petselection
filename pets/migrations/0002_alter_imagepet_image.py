# Generated by Django 3.2.6 on 2021-10-06 08:59

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pets', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagepet',
            name='image',
            field=models.ImageField(blank=True, default=django.utils.timezone.now, upload_to='pet_images/', verbose_name='Изображение'),
            preserve_default=False,
        ),
    ]
