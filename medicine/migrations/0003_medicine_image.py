# Generated by Django 3.2.6 on 2021-08-24 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicine', '0002_auto_20210817_0850'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicine',
            name='image',
            field=models.ImageField(null=True, upload_to='images/medicines'),
        ),
    ]
