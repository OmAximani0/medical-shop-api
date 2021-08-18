from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from django.http import JsonResponse
import json
from rest_framework import status
from store.models import Store
from rest_framework.response import Response
from medicine.models import Medicine, StoreMedicine
from .serializer import StoreSerializer


# add store
class AddStoreView(GenericAPIView):
    def post(self, requests):
        try:
            response = {}
            serializer = StoreSerializer(data=requests.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                response['msg'] = "Store added successfully"
                return Response(response, status=status.HTTP_201_CREATED)
            response['msg'] = serializer.errors
        except Exception as e:
            print(e)
            response['msg'] = str(e)
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


# get all stores
class GetAllStoreView(GenericAPIView):
    def post(self, requests):
        try:
            response = {}
            instance = Store.objects.all()
            serailizer = StoreSerializer(instance, many=True)
            return Response(serailizer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            response['msg'] = str(e)
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

# get store
class GetStoreView(GenericAPIView):
    def post(self, requests):
        try:
            response = {}
            instance = Store.objects.get(pk=requests.data['store_id'])
            serializer = StoreSerializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            response['msg'] = str(e)
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

# update store
class UpdateStoreView(APIView):
    def put(self, requests):
        try:
            response = {}
            instance = Store.objects.get(pk=requests.data['store_id'])
            serializer = StoreSerializer(instance, data=requests.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                response['msg'] = 'Store updated successfully'
                return Response(response, status=status.HTTP_200_OK)
            response['msg'] = serializer.errors
        except Exception as e:
            print(e)
            response["msg"] = str(e)
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        try:
            response = {}
            instance = Store.objects.get(pk=request.data['store_id'])
            serializer = StoreSerializer(instance, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                response['msg'] = 'Store updated successfully'
                return Response(response, status=status.HTTP_200_OK)
            response['msg'] = serializer.errors
        except Exception as e:
            print(e)
            response["msg"] = str(e)
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


# delete store
class DeleteStoreView(APIView):

    def delete(self, requests):
        try:
            response = {}
            instance = Store.objects.filter(pk=requests.data['store_id'])
            instance.delete()
            response['msg'] = 'Store deleted from database'
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            response["msg"] = str(e)
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


# stores by medicine
class StoresByMedicineView(GenericAPIView):
    def post(self, requests):
        try:
            requests = json.load(requests)
            medicines = requests.get("medicines")
            data = dict()
            for medicine_id in medicines:
                medicine = Medicine.objects.get(pk=medicine_id)
                store_medicines = StoreMedicine.objects.filter(medicine_id=medicine, quantity__gte=1)
                data[medicine_id] = list()
                for store_medicine in store_medicines:
                    data[medicine_id].append({
                        "store_id": store_medicine.store_id.store_id,
                        "store_name": store_medicine.store_id.store_name,
                        "store_phone_number": store_medicine.store_id.store_phone_number,
                        "store_address": store_medicine.store_id.store_address,
                        "quantity": store_medicine.quantity,
                        "price": store_medicine.price
                    })
            response = data
        except Exception as e:
            print(e)
            response = {"error": str(e)}
        return JsonResponse(response)
