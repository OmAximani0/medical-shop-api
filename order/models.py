from django.db import models

from users.models import Users
from store.models import Store
from medicine.models import Medicine

class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    store_id = models.ForeignKey(Store, on_delete=models.CASCADE)
    order_datetime = models.DateTimeField()
    order_fulfilment_datetime = models.DateTimeField(null=True)
    order_fulfilment_status = models.TextField(default="pending")
    total_amount = models.FloatField()

    class Meta: 
        db_table = 'order'


class OrderMedicine(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    medicine_id = models.ForeignKey(Medicine, on_delete=models.DO_NOTHING)
    order_quantity = models.IntegerField()

    class Meta:
        db_table = 'order_medicine'
        unique_together = (('order_id', 'medicine_id'),)
