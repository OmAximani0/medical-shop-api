# Generated by Django 3.2.6 on 2021-08-27 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicine', '0003_medicine_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='storemedicine',
            name='exp_date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='storemedicine',
            name='mfg_date',
            field=models.DateField(null=True),
        ),
    ]