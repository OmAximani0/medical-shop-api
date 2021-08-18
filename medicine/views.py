from rest_framework.generics import GenericAPIView
from django.http import JsonResponse
import json
from medicine.models import Medicine, StoreMedicine
from store.models import Store
from rest_framework import status
from rest_framework.response import Response

from .serializer import MedicineSerializer, StoreMedicineSerializer, NestedStoreMedicineSerializer


# add medicine
class AddMedicineView(GenericAPIView):
    def post(self, requests):
        try:
            response = {}
            serializer = MedicineSerializer(data=requests.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                response['msg'] = 'Medicine added successfully'
                return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            response["msg"] = str(e)
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


# get all medicines
class GetAllMedicineView(GenericAPIView):
    def post(self, requests):
        try:
            response = {}
            instance = Medicine.objects.all()
            serializer = MedicineSerializer(instance, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            response["msg"] = str(e)
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


# get medicine
class GetMedicineView(GenericAPIView):
    def post(self, requests):
        try:
            response = {}
            instacnce = Medicine.objects.get(pk=requests.data['medicine_id'])
            serializer = MedicineSerializer(instacnce)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            response["msg"] = str(e)
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


# update medicine
class UpdateMedicineView(GenericAPIView):
    def put(self, requests):
        try:
            response = {}
            instance = Medicine.objects.get(pk=requests.data['medicine_id'])
            serializer = MedicineSerializer(instance, data=requests.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                response['msg'] = 'Medicine updated successfully'
                return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            response["msg"] = str(e)
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


# delete medicine
class DeleteMedicineView(GenericAPIView):
    def post(self, requests):
        try:
            response = {}
            instance = Medicine.objects.filter(pk=requests.data['medicine_id'])
            instance.delete()
            response['msg'] = 'Medicine deleted successfully'
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            response["msg"] = str(e)
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


# add store medicine
class AddStoreMedicineView(GenericAPIView):
    def post(self, requests):
        try:
            response = {}
            serializer = StoreMedicineSerializer(data=requests.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                response['msg'] = 'Medicine added successfully'
                return Response(response, status=status.HTTP_200_OK)
            response['msg'] = serializer.error_messages
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            response["error"] = str(e)
        return Response(response , status=status.HTTP_400_BAD_REQUEST)


# get store medicine
class GetStoreMedicineView(GenericAPIView):
    def post(self, requests):
        try:
            response = {}
            instance = StoreMedicine.objects.filter(medicine_id = requests.data.get('medicine_id'))
            serializer = NestedStoreMedicineSerializer(instance, many=True)
            return Response(serializer.data , status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            response["error"] = str(e)
        return JsonResponse(response)


# update store medicine
class UpdateStoreMedicineView(GenericAPIView):
    def post(self, requests):
        try:
            requests = json.load(requests)
            store_medicines = requests.get("store_medicines")
            for store_medicine in store_medicines:
                store = Store.objects.get(pk=store_medicine["store_id"])
                medicines = store_medicine["update_medicines"]
                for medicine_obj in medicines:
                    medicine = Medicine.objects.get(pk=medicine_obj["medicine_id"])
                    StoreMedicine.objects.filter(store_id=store, medicine_id=medicine)\
                        .update(**medicine_obj["update"])
            response = {
                "message": "store medicines updated successfully"
            }
        except Exception as e:
            print(e)
            response = {"error": str(e)}
        return JsonResponse(response)


# delete store medicine
class DeleteStoreMedicineView(GenericAPIView):
    def post(self, requests):
        try:
            requests = json.load(requests)
            store_medicines = requests.get("store_medicines")
            for store_medicine_obj in store_medicines:
                store = Store.objects.get(pk=store_medicine_obj["store_id"])
                medicines = store_medicine_obj["medicines"]
                for medicine_id in medicines:
                    medicine = Medicine.objects.get(pk=medicine_id)
                    store_medicine = StoreMedicine.objects.get(store_id=store, medicine_id=medicine)
                    store_medicine.delete()
            response = {
                "message": "store medicines deleted successfully"
            }
        except Exception as e:
            print(e)
            response = {"error": str(e)}
        return JsonResponse(response)
