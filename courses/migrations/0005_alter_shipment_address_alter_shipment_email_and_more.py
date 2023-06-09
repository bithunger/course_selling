# Generated by Django 4.2.1 on 2023-05-16 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_shipment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shipment',
            name='address',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='shipment',
            name='email',
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name='shipment',
            name='telephone_number',
            field=models.CharField(max_length=20),
        ),
    ]
