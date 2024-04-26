import uuid
from codeia.models import User, Forgotten
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from email_system.send_email import email_forgotten_password
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import (
    ForgottenSerializers,
    VerifyForgotSerializers,
)

class ForgottenPasswordView(generics.CreateAPIView):
    serializer_class = ForgottenSerializers
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        return serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=False)
        link = str(uuid.uuid4())
        forgot = Forgotten.objects.filter(email=serializer.validated_data['email'])
        if len(forgot) > 0:
            return Response({'message': 'The link has already been sent to your email', 'status': True})
        user = get_object_or_404(User, email=serializer.validated_data['email'])
        if user.is_unverified:
            return Response({'message': 'You need to verify your email first', 'status': False})
        serializer.validated_data['link'] = link
        email_forgotten_password(user.email, user.name + ' ' + user.surname, link)
        serializer.save()
        return Response({'message': 'Link has been sent to your email', 'status': True})
    
class ChangePasswordView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = VerifyForgotSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)