# Generated by Django 2.1.5 on 2019-02-27 11:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0007_auto_20190227_1106'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='band',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='music.Band', verbose_name='Zespół'),
            preserve_default=False,
        ),
    ]
