# Generated by Django 4.2.1 on 2024-03-05 01:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userauths', '0005_alter_profile_image_alter_profile_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='image'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='phone',
            field=models.CharField(blank=True, max_length=14, null=True),
        ),
    ]
