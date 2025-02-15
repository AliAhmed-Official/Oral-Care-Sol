# Generated by Django 4.2.1 on 2024-02-12 09:11

from django.db import migrations, models
import django.db.models.deletion
import shortuuid.django_fields


class Migration(migrations.Migration):

    dependencies = [
        ('OCS_APP', '0009_address_mobile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Manufacturer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mid', shortuuid.django_fields.ShortUUIDField(alphabet='abcdefgh12345', length=10, max_length=20, prefix='manuf', unique=True)),
                ('title', models.CharField(default='Local', max_length=100)),
            ],
            options={
                'verbose_name_plural': 'Manufacturers',
            },
        ),
        migrations.RemoveField(
            model_name='product',
            name='vendor',
        ),
        migrations.DeleteModel(
            name='Vendor',
        ),
        migrations.AddField(
            model_name='product',
            name='manufacturer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='OCS_APP.manufacturer'),
        ),
    ]
