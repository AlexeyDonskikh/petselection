# Generated by Django 3.2.6 on 2021-09-29 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pets', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pet',
            name='weight',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, verbose_name='Возраст'),
        ),
    ]