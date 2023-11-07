from rest_framework_simplejwt.authentication import JWTAuthentication
from codeia.models import FAQ
from rest_framework import generics
from codeia.permissions import IsAdminUser
from .serializers import (
    FAQSerializers,
)

class ListFAQView(generics.ListAPIView):
    serializer_class = FAQSerializers
    authentication_classes = [JWTAuthentication]  # Autenticacion
    permission_classes = [IsAdminUser]  # Permisos
    queryset = FAQ.objects.all().order_by('id')

class GetFAQView(generics.RetrieveAPIView):
    serializer_class = FAQSerializers
    authentication_classes = [JWTAuthentication]  # Autenticacion
    permission_classes = [IsAdminUser]  # Permisos
    queryset = FAQ.objects.all()

    def get_queryset(self):
        return self.queryset.filter(id=self.kwargs['pk'])
    
class CreateFAQView(generics.CreateAPIView):
    serializer_class = FAQSerializers
    authentication_classes = [JWTAuthentication]  # Autenticacion
    permission_classes = [IsAdminUser]  # Permisos
    queryset = FAQ.objects.all()

class UpdateFAQView(generics.UpdateAPIView):
    serializer_class = FAQSerializers
    authentication_classes = [JWTAuthentication]  # Autenticacion
    permission_classes = [IsAdminUser]  # Permisos
    queryset = FAQ.objects.all()

    def get_object(self):
        return self.queryset.get(id=self.kwargs['pk'])

class DeleteFAQView(generics.DestroyAPIView):
    serializer_class = FAQSerializers
    authentication_classes = [JWTAuthentication]  # Autenticacion
    permission_classes = [IsAdminUser]  # Permisos
    queryset = FAQ.objects.all()

    def get_object(self):
        return self.queryset.get(id=self.kwargs['pk'])