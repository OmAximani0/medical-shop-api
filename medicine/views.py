from rest_framework.generics import GenericAPIView
from django.http import JsonResponse
import json
from medicine.models import Medicine, StoreMedicine
from store.models import Store
from uuid import uuid4


# add medicine
class AddMedicineView(GenericAPIView):
    def post(self, requests):
        try:
            requests = json.load(requests)
            medicines = requests.get("medicines")
            for medicine in medicines:
                medicine_id = uuid4()
                medicine_name = medicine["medicine_name"]
                new_medicine = Medicine(medicine_id=medicine_id, medicine_name=medicine_name)
                new_medicine.save()

            response = {
                "message": "medicine created successfully"
            }
        except Exception as e:
            print(e)
            response = {"error": str(e)}
        return JsonResponse(response)


# get all medicines
class GetAllMedicineView(GenericAPIView):
    def post(self, requests):
        try:
            data = []
            medicines = Medicine.objects.all()
            for medicine in medicines:
                data.append({
                    "medicine_id": medicine.medicine_id,
                    "medicine_name": medicine.medicine_name,
                })
            response = {
                "data": data
            }
        except Exception as e:
            print(e)
            response = {"error": str(e)}
        return JsonResponse(response)


# get medicine
class GetMedicineView(GenericAPIView):
    def post(self, requests):
        try:
            requests = json.load(requests)
            medicines = requests.get("medicines")
            data = []
            for medicine_id in medicines:
                medicine_obj = Medicine.objects.get(pk=medicine_id)
                data.append({
                    "medicine_id": medicine_obj.medicine_id,
                    "medicine_name": medicine_obj.medicine_name
                })
            response = {
                "data": data
            }
        except Exception as e:
            print(e)
            response = {"error": str(e)}
        return JsonResponse(response)


# update medicine
class UpdateMedicineView(GenericAPIView):
    def post(self, requests):
        try:
            requests = json.load(requests)
            medicines = requests.get("medicines")
            for medicine in medicines:
                Medicine.objects.filter(pk=medicine["medicine_id"]).update(**medicine["update"])
            response = {
                "message": "medicines updated successfully"
            }
        except Exception as e:
            print(e)
            response = {"error": str(e)}
        return JsonResponse(response)


# delete medicine
class DeleteMedicineView(GenericAPIView):
    def post(self, requests):
        try:
            requests = json.load(requests)
            medicines = requests.get("medicines")
            for medicine_id in medicines:
                medicine = Medicine.objects.get(pk=medicine_id)
                medicine.delete()
            response = {
                "message": "medicine deleted successfully"
            }
        except Exception as e:
            print(e)
            response = {"error": str(e)}
        return JsonResponse(response)


# add store medicine
class AddStoreMedicineView(GenericAPIView):
    def post(self, requests):
        try:
            requests = json.load(requests)
            store_medicines = requests.get("store_medicines")
            for store_medicine in store_medicines:
                store = Store.objects.get(pk=store_medicine["store_id"])
                medicines = store_medicine["medicines"]
                for medicine_obj in medicines:
                    medicine = Medicine.objects.get(pk=medicine_obj["medicine_id"])
                    new_store_medicine = StoreMedicine(store_id=store, medicine_id=medicine,
                                                       quantity=medicine_obj["quantity"],
                                                       price=medicine_obj["price"])
                    new_store_medicine.save()
            response = {
                "message": "medicines added to stores successfully"
            }
        except Exception as e:
            print(e)
            response = {"error": str(e)}
        return JsonResponse(response)


# get store medicine
class GetStoreMedicineView(GenericAPIView):
    def post(self, requests):
        try:
            requests = json.load(requests)
            stores = requests.get("stores")
            data = dict()
            for store_id in stores:
                store = Store.objects.get(pk=store_id)
                store_medicines = StoreMedicine.objects.filter(store_id=store)
                data[store_id] = list()
                for store_medicine in store_medicines:
                    data[store_id].append({
                        "medicine_id": store_medicine.medicine_id.medicine_id,
                        "medicine_name": store_medicine.medicine_id.medicine_name,
                        "quantity": store_medicine.quantity,
                        "price": store_medicine.price
                    })
            response = data
        except Exception as e:
            print(e)
            response = {"error": str(e)}
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
