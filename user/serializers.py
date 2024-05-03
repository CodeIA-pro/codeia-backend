from django.contrib.auth import (
    get_user_model,
)
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from email_system.send_email import generate_code, email_verify
from codeia.models import User

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        token = self.get_token(self.user)
        data["user"] = str(self.user)
        data["id"] = self.user.id
        userprofile = get_object_or_404(User, email=self.user)
        if userprofile.is_unverified:
            return {'status': True}
        if userprofile.two_factor:
            code = generate_code()
            userprofile.verification_code = code
            userprofile.save()
            email_verify(userprofile.email, userprofile.name + " " + userprofile.surname, code)
            return {'two_factor': True}
        data["role"] = userprofile.role
        data["name"] = userprofile.name + " " + userprofile.surname
        data["repo_login"] = userprofile.repo_login
        return data
    
class MyTokenTwoFASerializer(serializers.Serializer):
    code = serializers.IntegerField()

    def validate(self, attrs):
        code = attrs.get('code')
        user = get_object_or_404(User, verification_code=code)
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'id': user.id,
            'user': user.email,
            'name': f"{user.name} {user.surname}",
            'role': user.role,
            'repo_login': user.repo_login,
        }
    
class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ["id","email", "name", "surname", "date_of_birth", "role", "password",]
        read_only_fields = ["id","role",]


class CheckSerializer(serializers.Serializer):
    code = serializers.IntegerField()

class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = get_user_model()
        fields = ["id", "email", "name", "surname", "password", "two_factor", "repo_login", "full_name", "user_github"]
        read_only_fields = ["id", "created_at", "role",]

    def get_full_name(self, obj):
        return f"{obj.name} {obj.surname}"

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
        fields = ["id", "email", "name", "surname", "date_of_birth", "role", "created_at",]
        read_only_fields = ["id", "created_at",]

class UserSerializerAdminUpdate(serializers.ModelSerializer):
     class Meta:
        model = get_user_model()
        fields = ["id", "email", "name", "surname", "date_of_birth", "role", "created_at",]
        read_only_fields = ["id", "created_at","email"]

class UserPassSerializer(serializers.Serializer):
    pass