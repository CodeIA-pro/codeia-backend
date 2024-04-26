from rest_framework import serializers
from codeia.models import Forgotten, User
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404

class ForgottenSerializers(serializers.ModelSerializer):
    class Meta:
        model = Forgotten
        fields = ['id', 'email']
        read_only_fields = ['id',]

class VerifyForgotSerializers(serializers.Serializer):
    code = serializers.CharField()
    password = serializers.CharField()

    def save(self):
        code = self.validated_data['code']
        forgot = get_object_or_404(Forgotten, link=code)
        user = get_object_or_404(User, email=forgot.email)
        password = self.validated_data['password']
        user.password = make_password(password)
        user.save()
        forgot.delete()
        return {'status': True}