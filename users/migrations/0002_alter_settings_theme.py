# Generated by Django 4.2.3 on 2023-07-11 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='settings',
            name='theme',
            field=models.CharField(blank=True, choices=[('', 'Atena Default'), ('asuna', 'Yuuki Asuna (Day)'), ('asuna-dark', 'Yuuki Asuna (Night)'), ('suisei', 'Hoshimachi Suisei (Day)')], default='', max_length=20),
        ),
    ]