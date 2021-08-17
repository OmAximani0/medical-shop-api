from django.db import models

from store.models import Store


class Medicine(models.Model):
    medicine_id = models.AutoField(primary_key=True)
    medicine_name = models.TextField(unique=True)

    class Meta:
        db_table = 'medicine'

    def __str__(self):
        return self.medicine_name


class StoreMedicine(models.Model):
    store_id = models.ForeignKey(Store, on_delete=models.CASCADE)
    medicine_id = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()

    class Meta:
        db_table = 'store_medicine'
        unique_together = (('store_id', 'medicine_id'),)
