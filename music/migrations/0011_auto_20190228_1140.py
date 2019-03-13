# Generated by Django 2.1.5 on 2019-02-28 11:40

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0010_album_creation_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='album',
            name='creation_date',
        ),
        migrations.RemoveField(
            model_name='band',
            name='creation_date',
        ),
        migrations.AddField(
            model_name='album',
            name='creation_year',
            field=models.PositiveSmallIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1800), django.core.validators.MaxValueValidator(2019)], verbose_name='Rok założenia'),
        ),
        migrations.AddField(
            model_name='band',
            name='creation_year',
            field=models.PositiveSmallIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1800), django.core.validators.MaxValueValidator(2019)], verbose_name='Rok założenia'),
        ),
    ]
