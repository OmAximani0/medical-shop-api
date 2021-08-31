from rest_framework.views import APIView
from rest_framework import status
from store.models import Store
from rest_framework.response import Response
from medicine.models import StoreMedicine
from .serializer import StoreSerializer
from medicine.serializer import NestedStoreMedicineSerializer
from users.models import Users
from users.serializers import UserSerializer

# add store
class AddStoreView(APIView):
    def post(self, requests):
        try:
            response = {}
            user_id = requests.data['user_id']
            user_instance = Users.objects.get(pk=user_id)
            user_serializer = UserSerializer(user_instance)
            if user_serializer.data.get('role_name').lower() == "customer":
                response['msg'] = 'Only Seller can create Store'
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
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
class GetAllStoreView(APIView):
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
class GetStoreView(APIView):
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
class StoresByMedicineView(APIView):
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
