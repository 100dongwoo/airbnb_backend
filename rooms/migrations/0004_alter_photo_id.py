# Generated by Django 3.2.11 on 2022-01-08 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0003_alter_room_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
    ]
