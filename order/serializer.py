from rest_framework import serializers

from users.serializers import UserSerializer
from .models import Order, OrderMedicine
from medicine.serializer import MedicineSerializer

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        
class NestedOrderSerializer(serializers.ModelSerializer):

    user_id = UserSerializer()

    class Meta:
        model = Order
        fields = '__all__'

class NestedOrderMedicineSerializer(serializers.ModelSerializer):

    order_id = NestedOrderSerializer()
    medicine_id = MedicineSerializer()

    class Meta:
        model = OrderMedicine
        fields = '__all__'