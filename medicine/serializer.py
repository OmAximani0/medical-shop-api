from rest_framework import serializers

from .models import Medicine, StoreMedicine
from store.serializer import StoreSerializer

class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = '__all__'

class StoreMedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreMedicine
        fields = '__all__'

class NestedStoreMedicineSerializer(serializers.ModelSerializer):
    medicine_id = MedicineSerializer()
    store_id = StoreSerializer()
    class Meta:
        model = StoreMedicine
        fields = '__all__'