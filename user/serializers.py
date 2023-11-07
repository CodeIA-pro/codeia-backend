from django.contrib.auth import (
    get_user_model,
)
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.shortcuts import get_object_or_404
from codeia.models import User

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        token = self.get_token(self.user)
        data["user"] = str(self.user)
        data["id"] = self.user.id
        userprofile = get_object_or_404(User, email=self.user)
        data["role"] = userprofile.role
        return data
    
class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ["id","email", "name", "surname", "nationality", "date_of_birth", "role", "password",]
        read_only_fields = ["id","role",]


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = get_user_model()
        fields = ["id", "email", "name", "surname", "nationality", "date_of_birth", "role", "created_at", "password"]
        read_only_fields = ["id", "created_at", "role",]

    def __init__(self, *args, **kwargs):
        super(UserSerializer, self).__init__(*args, **kwargs)

        # Remove the password field for non-PATCH operations.
        if self.context.get('request') and self.context['request'].method != 'PATCH':
            self.fields.pop('password', None)


    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user
    
class UserSerializerAdmin(serializers.ModelSerializer):
     class Meta:
        model = get_user_model()
        fields = ["id", "email", "name", "surname", "nationality", "date_of_birth", "role", "created_at",]
        read_only_fields = ["id", "created_at",]

class UserSerializerAdminUpdate(serializers.ModelSerializer):
     class Meta:
        model = get_user_model()
        fields = ["id", "email", "name", "surname", "nationality", "date_of_birth", "role", "created_at",]
        read_only_fields = ["id", "created_at","email"]