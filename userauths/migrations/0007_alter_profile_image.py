# Generated by Django 4.2.1 on 2024-03-05 02:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userauths', '0006_alter_profile_image_alter_profile_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, upload_to='image'),
        ),
    ]
