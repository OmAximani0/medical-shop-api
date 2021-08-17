from django.db import models

from users.models import Users

class Store(models.Model):
    store_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    store_name = models.TextField()
    store_phone_number = models.TextField(unique=True)
    store_address = models.TextField()

    class Meta:
        db_table = 'store'

    def __str__(self):
        return self.store_name
