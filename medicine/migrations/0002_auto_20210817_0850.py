# Generated by Django 3.2.6 on 2021-08-17 03:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('medicine', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='medicine',
            table='medicine',
        ),
        migrations.AlterModelTable(
            name='storemedicine',
            table='store_medicine',
        ),
    ]
