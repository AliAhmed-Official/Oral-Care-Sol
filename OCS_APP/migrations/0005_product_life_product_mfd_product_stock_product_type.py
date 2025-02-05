# Generated by Django 4.2.1 on 2023-09-26 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OCS_APP', '0004_alter_productimages_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='life',
            field=models.CharField(blank=True, default='100 Days', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='mfd',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='stock',
            field=models.IntegerField(blank=True, default='1', null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='type',
            field=models.CharField(blank=True, default='Dental Product', max_length=100, null=True),
        ),
    ]
