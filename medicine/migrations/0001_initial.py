# Generated by Django 3.2.6 on 2021-08-17 03:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Medicine',
            fields=[
                ('medicine_id', models.AutoField(primary_key=True, serialize=False)),
                ('medicine_name', models.TextField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='StoreMedicine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('price', models.FloatField()),
                ('medicine_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medicine.medicine')),
                ('store_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.store')),
            ],
            options={
                'unique_together': {('store_id', 'medicine_id')},
            },
        ),
    ]
