from rest_framework_simplejwt.authentication import JWTAuthentication
from codeia.models import Plan
from rest_framework import generics
from codeia.permissions import IsAdminUser
from .serializers import (
    PlanSerializers,
)

class ListPlanView(generics.ListAPIView):
    serializer_class = PlanSerializers
    authentication_classes = [JWTAuthentication]  # Autenticacion
    permission_classes = [IsAdminUser]  # Permisos
    queryset = Plan.objects.all().order_by('id')

class GetPlanView(generics.RetrieveAPIView):
    serializer_class = PlanSerializers
    authentication_classes = [JWTAuthentication]  # Autenticacion
    permission_classes = [IsAdminUser]  # Permisos
    queryset = Plan.objects.all()

    def get_queryset(self):
        return self.queryset.filter(id=self.kwargs['pk'])
    
class CreatePlanView(generics.CreateAPIView):
    serializer_class = PlanSerializers
    authentication_classes = [JWTAuthentication]  # Autenticacion
    permission_classes = [IsAdminUser]  # Permisos
    queryset = Plan.objects.all()

class UpdatePlanView(generics.UpdateAPIView):
    serializer_class = PlanSerializers
    authentication_classes = [JWTAuthentication]  # Autenticacion
    permission_classes = [IsAdminUser]  # Permisos
    queryset = Plan.objects.all()

    def get_object(self):
        return self.queryset.get(id=self.kwargs['pk'])

class DeletePlanView(generics.DestroyAPIView):
    serializer_class = PlanSerializers
    authentication_classes = [JWTAuthentication]  # Autenticacion
    permission_classes = [IsAdminUser]  # Permisos
    queryset = Plan.objects.all()

    def get_object(self):
        return self.queryset.get(id=self.kwargs['pk'])