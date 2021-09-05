from rest_framework import serializers
from .models import Users
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from store.serializer import StoreSerializer
from store.models import Store

class UserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user

    class Meta:
        model = Users
        fields = '__all__'


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        # Add extra responses here
        data['user_name'] = self.user.user_name
        data['user_email'] = self.user.user_email
        data['role'] = self.user.role_name
        data['user_id'] = self.user.user_id
        
        if data['role'].lower() == "seller":
            try:
                user_id = self.user.user_id
                instance = Store.objects.get(user_id=user_id)
                serializer = StoreSerializer(instance)
                data['store_id'] = serializer.data.get('store_id')
            except Exception as e:
                print(e)

        return data 
