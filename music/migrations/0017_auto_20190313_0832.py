# Generated by Django 2.1.5 on 2019-03-13 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0016_auto_20190313_0824'),
    ]

    operations = [
        migrations.AlterField(
            model_name='band',
            name='spotify_follow',
            field=models.TextField(blank=True, max_length=255, null=True, verbose_name='Przycisk obserwowania Spotify'),
        ),
        migrations.AlterField(
            model_name='band',
            name='spotify_play',
            field=models.TextField(blank=True, max_length=255, null=True, verbose_name='Przycisk odtwarzania Spotify'),
        ),
    ]