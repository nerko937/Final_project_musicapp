# Generated by Django 2.1.5 on 2019-02-22 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='modification_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
