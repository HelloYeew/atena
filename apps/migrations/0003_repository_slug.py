# Generated by Django 4.2.3 on 2023-07-10 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0002_alter_repository_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='repository',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, unique=True),
        ),
    ]
