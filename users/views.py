from django.shortcuts import render
from rest_framework.response import Response
from django.http import HttpResponseBadRequest
from .serializers import UserSerializer
from django.contrib.auth.models import User, update_last_login
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTokenObtainPairSerializer
from rest_framework.views import APIView
from rest_framework import status
from users import serializers
from .models import Users
from rest_framework.permissions import IsAuthenticated

class AddUser(APIView):

	#permission_classes = [IsAuthenticated]
	def post(self, request):
		response = {}
		serializer = UserSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			response['message'] = "User created successfull"
			response_status = status.HTTP_200_OK
		else:
			response['error'] = serializer.errors
			response_status = status.HTTP_400_BAD_REQUEST

		return Response(response, status=response_status)


class GetAllUsers(APIView):

	#   permission_classes = [IsAuthenticated]
	def get(self, request):
		try:
			users = Users.objects.all()
		except:
			return Response(status=status.HTTP_400_BAD_REQUEST)
		list_of_users = []
		user_object = {}

		for user in users:
			user_object['user_name'] = user.user_name
			user_object['date_joined'] = user.date_joined
			list_of_users.append(user_object)
			user_object = {}
		return Response(list_of_users, status=status.HTTP_200_OK)


class GetUser(APIView):
	def get(self, request):
		instance = Users.objects.get(user_id=request.data.get['user_id'])
		serializer = UserSerializer(instance)
		return Response(serializer.data, status=status.HTTP_200_OK)

class UpdateUser(APIView):
	def put(self, request):
		response = {}
		try:
			instance = Users.objects.get(user_id=request.data['user_id'])
			serializer = UserSerializer(instance, data=request.data)
			if serializer.is_valid(raise_exception=True):
				serializer.save()
				response['msg'] = 'User updated successfully'
				return Response(response, status=status.HTTP_200_OK)
			response['msg'] = serializer.errors	
		except Exception as e:
			response['msg'] = str(e)
		return Response(response, status=status.HTTP_400_BAD_REQUEST)

	def patch(self, request):
		response = {}
		try:
			instance = Users.objects.get(user_id=request.data['user_id'])
			serializer = UserSerializer(instance, data=request.data, partial=True)
			if serializer.is_valid(raise_exception=True):
				serializer.save()
				response['msg'] = 'User updated successfully'
				return Response(response, status=status.HTTP_200_OK)
			response['msg'] = serializer.errors	
		except Exception as e:
			response['msg'] = str(e)
		return Response(response, status=status.HTTP_400_BAD_REQUEST)

class DeleteUser(APIView):
	def delete(self, request):
		response = {}
		try:
			instance = Users.objects.filter(user_id = request.data['user_id'])
			instance.delete()
			response['msg'] = "User deleted successfully"
			return Response(response, status=status.HTTP_200_OK)
		except Exception as e:
			response['msg'] = e
			return Response(response, status=status.HTTP_400_BAD_REQUEST)


class MyTokenObtainPairView(TokenObtainPairView):
	serializer_class = MyTokenObtainPairSerializer
