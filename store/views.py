from rest_framework.generics import GenericAPIView
from django.http import JsonResponse
import json
from store.models import Store
from users.models import Users
from medicine.models import Medicine, StoreMedicine
from uuid import uuid4


# add store
class AddStoreView(GenericAPIView):
    def post(self, requests):
        try:
            requests = json.load(requests)
            stores = requests.get("stores")
            for store in stores:
                user = Users.objects.get(pk=store["user_id"])
                store_id = uuid4()
                store_name = store["store_name"]
                store_phone_number = store["store_phone_number"]
                store_address = store["store_address"]
                new_store = Store(store_id=store_id, user_id=user, store_name=store_name,
                                  store_phone_number=store_phone_number, store_address=store_address)
                new_store.save()

            response = {
                "message": "store created successfully"
            }
        except Exception as e:
            print(e)
            response = {"error": str(e)}
        return JsonResponse(response)


# get all stores
class GetAllStoreView(GenericAPIView):
    def post(self, requests):
        try:
            data = []
            stores = Store.objects.all()
            for store in stores:
                data.append({
                    "user_id": store.user_id.user_id,
                    "store_id": store.store_id,
                    "store_name": store.store_name,
                    "store_phone_number": store.store_phone_number,
                    "store_address": store.store_address,
                })
            response = {
                "data": data
            }
        except Exception as e:
            print(e)
            response = {"error": str(e)}
        return JsonResponse(response)


# get store
class GetStoreView(GenericAPIView):
    def post(self, requests):
        try:
            requests = json.load(requests)
            stores = requests.get("stores")
            data = []
            for store_id in stores:
                store_obj = Store.objects.get(pk=store_id)
                data.append({
                    "store_id": store_obj.store_id,
                    "store_name": store_obj.store_name,
                    "store_phone_number": store_obj.store_phone_number,
                    "store_address": store_obj.store_address
                })
            response = {
                "data": data
            }
        except Exception as e:
            print(e)
            response = {"error": str(e)}
        return JsonResponse(response)


# update store
class UpdateStoreView(GenericAPIView):
    def post(self, requests):
        try:
            requests = json.load(requests)
            stores = requests.get("stores")
            for store in stores:
                Store.objects.filter(pk=store["store_id"]).update(**store["update"])
            response = {
                "message": "store updated successfully"
            }
        except Exception as e:
            print(e)
            response = {"error": str(e)}
        return JsonResponse(response)


# delete store
class DeleteStoreView(GenericAPIView):
    def post(self, requests):
        try:
            requests = json.load(requests)
            stores = requests.get("stores")
            for store_id in stores:
                store = Store.objects.get(pk=store_id)
                store.delete()
            response = {
                "message": "store deleted successfully"
            }
        except Exception as e:
            print(e)
            response = {"error": str(e)}
        return JsonResponse(response)


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
