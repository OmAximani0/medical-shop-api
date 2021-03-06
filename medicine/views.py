from medicine.models import Medicine, StoreMedicine
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser, FileUploadParser
from django.http.response import JsonResponse

from .serializer import MedicineSerializer, StoreMedicineSerializer, NestedStoreMedicineSerializer


# add medicine
class AddMedicineView(APIView):

    parser_classes = [
        MultiPartParser,
        FormParser,
        FileUploadParser,
        JSONParser,
    ]

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
class GetAllMedicineView(APIView):
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
class GetMedicineView(APIView):
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
class UpdateMedicineView(APIView):
    def put(self, requests):
        try:
            response = {}
            instance = Medicine.objects.get(pk=requests.data['medicine_id'])
            serializer = MedicineSerializer(instance, data=requests.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                response['msg'] = 'Medicine updated successfully'
                return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            response["msg"] = str(e)
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


# delete medicine
class DeleteMedicineView(APIView):
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
class AddStoreMedicineView(APIView):
    def post(self, requests):
        try:
            response = {}
            serializer = StoreMedicineSerializer(data=requests.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                response['msg'] = 'Medicine added to store successfully'
                return Response(response, status=status.HTTP_200_OK)
            response['msg'] = serializer.error_messages
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            response["error"] = str(e)
        return Response(response , status=status.HTTP_400_BAD_REQUEST)


# all store medicine

class AllStoreMedicine(APIView):
    def get(self, request):
        try:
            response = []
            storemedicines = StoreMedicine.objects.all()
            serializer = NestedStoreMedicineSerializer(storemedicines, many=True)
            store_medicine_object = {}
            for store_medicine in serializer.data:
                store_medicine_object['store_name'] = store_medicine['store_id']['store_name']
                store_medicine_object['medicine_name'] = store_medicine['medicine_id']['medicine_name']
                store_medicine_object['store_phone'] = store_medicine['store_id']['store_phone_number']
                store_medicine_object['medicine_image'] = str(store_medicine['medicine_id']['image'])
                store_medicine_object['store_address'] = store_medicine['store_id']['store_address']
                store_medicine_object['price'] = store_medicine['price']
                response.append(store_medicine_object)
                store_medicine_object = {}
            return JsonResponse(response, safe=False, status=status.HTTP_200_OK)
            
        except Exception as e:
            print(e)    
            return JsonResponse(response,safe=False, status=status.HTTP_400_BAD_REQUEST)


# get store medicine
class GetStoreMedicineView(APIView):
    def post(self, requests):
        try:
            response = {}
            instance = StoreMedicine.objects.filter(store_id = requests.data.get('store_id'))
            serializer = NestedStoreMedicineSerializer(instance, many=True)
            return Response(serializer.data , status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            response["error"] = str(e)
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


# update store medicine
class UpdateStoreMedicineView(APIView):
    def post(self, requests):
        try:
            response = {}
            store_id = requests.data['store_id']
            medicine_id = requests.data['medicine_id']
            instance = StoreMedicine.objects.get(store_id=store_id, medicine_id=medicine_id)
            if 'quantity' in requests.data:
                requests.data['quantity'] += instance.quantity
            serializer = StoreMedicineSerializer(instance, data=requests.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                response['msg'] = "Medicine updated successfully"
                return Response(response, status=status.HTTP_200_OK)
            response["msg"] = serializer.error_messages
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            response["error"] = str(e)
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

# delete store medicine
class DeleteStoreMedicineView(APIView):
    def post(self, requests):
        try:
            response = {}
            store_id = requests.data['store_id']
            medicine_id = requests.data['medicine_id']
            exists = StoreMedicine.objects.filter(store_id=store_id, medicine_id=medicine_id).exists()
            if exists:
                StoreMedicine.objects.filter(store_id=store_id, medicine_id=medicine_id).delete()
                response['msg'] = 'Medicine deleted successfully'
                return Response(response, status=status.HTTP_200_OK)
            response['msg'] = 'Medcine does not exists'
        except Exception as e:
            print(e)
            response["error"] = str(e)
        return Response(response, status=status.HTTP_400_BAD_REQUEST)



#search in which store medicine is available
class SearchMedicine(APIView):
    def post(self,requests):
        response = []
        medicine_name = requests.data["medicine_name"]
        print(medicine_name)
        try:
            medicines = Medicine.objects.filter(medicine_name__contains=medicine_name)
            medicine_ids = [medicine.medicine_id for medicine in medicines]
            storemedicines = StoreMedicine.objects.filter(medicine_id__in=medicine_ids)
            serializer = NestedStoreMedicineSerializer(storemedicines, many=True)
            store_medicine_object = {}
            for store_medicine in serializer.data:
                    store_medicine_object['store_id'] = store_medicine['store_id']['store_id']
                    store_medicine_object['store_name'] = store_medicine['store_id']['store_name']
                    store_medicine_object['medicine_name'] = store_medicine['medicine_id']['medicine_name']
                    store_medicine_object['store_phone'] = store_medicine['store_id']['store_phone_number']
                    store_medicine_object['medicine_image'] = str(store_medicine['medicine_id']['image'])
                    store_medicine_object['store_address'] = store_medicine['store_id']['store_address']
                    store_medicine_object['price'] = store_medicine['price']
                    response.append(store_medicine_object)
                    store_medicine_object = {}
            return JsonResponse(response, safe=False, status=status.HTTP_200_OK)  
        except Exception as e:
            print(e)
            return JsonResponse(response, safe=False, status=status.HTTP_400_BAD_REQUEST)    