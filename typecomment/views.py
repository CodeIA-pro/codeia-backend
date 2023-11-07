from rest_framework_simplejwt.authentication import JWTAuthentication
from codeia.models import TypeComment
from rest_framework import generics
from codeia.permissions import IsAdminUser, IsGuestUser
from .serializers import (
    TypeCommentSerializers,
)

class ListTypeCommentView(generics.ListAPIView):
    serializer_class = TypeCommentSerializers
    permission_classes = [IsGuestUser]  # Permisos
    queryset = TypeComment.objects.all().order_by('id')

class GetTypeCommentView(generics.RetrieveAPIView):
    serializer_class = TypeCommentSerializers
    authentication_classes = [JWTAuthentication]  # Autenticacion
    permission_classes = [IsAdminUser]  # Permisos
    queryset = TypeComment.objects.all()

    def get_queryset(self):
        return self.queryset.filter(id=self.kwargs['pk'])
    
class CreateTypeCommentView(generics.CreateAPIView):
    serializer_class = TypeCommentSerializers
    authentication_classes = [JWTAuthentication]  # Autenticacion
    permission_classes = [IsAdminUser]  # Permisos
    queryset = TypeComment.objects.all()

class UpdateTypeCommentView(generics.UpdateAPIView):
    serializer_class = TypeCommentSerializers
    authentication_classes = [JWTAuthentication]  # Autenticacion
    permission_classes = [IsAdminUser]  # Permisos
    queryset = TypeComment.objects.all()

    def get_object(self):
        return self.queryset.get(id=self.kwargs['pk'])

class DeleteTypeCommentView(generics.DestroyAPIView):
    serializer_class = TypeCommentSerializers
    authentication_classes = [JWTAuthentication]  # Autenticacion
    permission_classes = [IsAdminUser]  # Permisos
    queryset = TypeComment.objects.all()

    def get_object(self):
        return self.queryset.get(id=self.kwargs['pk'])