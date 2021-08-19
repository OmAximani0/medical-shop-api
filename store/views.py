from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework import status
from store.models import Store
from rest_framework.response import Response
from medicine.models import StoreMedicine
from .serializer import StoreSerializer
from medicine.serializer import NestedStoreMedicineSerializer

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
            response = {}
            instance = StoreMedicine.objects.filter(medicine_id = requests.data['medicine_id'], quantity__gte=1)
            serializer = NestedStoreMedicineSerializer(instance, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            response["error"] = str(e)
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
