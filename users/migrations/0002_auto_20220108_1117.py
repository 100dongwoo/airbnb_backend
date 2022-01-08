# Generated by Django 2.2.5 on 2022-01-08 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, upload_to='avatars'),
        ),
        migrations.AlterField(
            model_name='user',
            name='favs',
            field=models.ManyToManyField(blank=True, related_name='favs', to='rooms.Room'),
        ),
    ]
