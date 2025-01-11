# Generated by Django 4.2.3 on 2023-07-10 18:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0004_repositorypermission'),
    ]

    operations = [
        migrations.CreateModel(
            name='RepositoryAPIKey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=32, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('repository', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='api_keys', to='apps.repository')),
            ],
        ),
    ]
