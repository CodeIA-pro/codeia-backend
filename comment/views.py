from rest_framework_simplejwt.authentication import JWTAuthentication
from codeia.models import Comment, TypeComment
from rest_framework import generics
from codeia.permissions import IsAuthenticatedUser
from django.shortcuts import get_object_or_404 
from .serializers import (
    CommentSerializers,
    ListCommentSerializers
)

class ListCommentView(generics.ListAPIView):
    serializer_class = ListCommentSerializers
    authentication_classes = [JWTAuthentication]  # Autenticacion
    permission_classes = [IsAuthenticatedUser]  # Permisos
    
    def get_queryset(self):
        type_id = self.kwargs['type_id']
        type_comment = get_object_or_404(TypeComment, pk=type_id)
        return Comment.objects.filter(type_comment=type_comment.id).order_by('id')
    
class GetCommentbyUserView(generics.ListAPIView):
    serializer_class = ListCommentSerializers
    authentication_classes = [JWTAuthentication]  # Autenticacion
    permission_classes = [IsAuthenticatedUser]  # Permisos
    
    def get_queryset(self):
        return Comment.objects.filter(user=self.request.user.id).order_by('id')
    
class CreateCommentView(generics.CreateAPIView):
    serializer_class = CommentSerializers
    authentication_classes = [JWTAuthentication]  # Autenticacion
    permission_classes = [IsAuthenticatedUser]  # Permisos
    
    def perform_create(self, serializer):
        type_id = self.kwargs['type_id']
        type_comment = get_object_or_404(TypeComment, pk=type_id)
        data = dict(serializer.validated_data)
        data['user'] = self.request.user.id
        data['type_comment'] = type_comment.id
        serializer.save(**data)
        return serializer.data

class UpdateCommentView(generics.UpdateAPIView):
    serializer_class = CommentSerializers
    authentication_classes = [JWTAuthentication]  # Autenticacion
    permission_classes = [IsAuthenticatedUser]  # Permisos
    queryset = Comment.objects.all()

    def get_object(self):
        return self.queryset.get(id=self.kwargs['pk'])

class DeleteCommentView(generics.DestroyAPIView):
    serializer_class = CommentSerializers
    authentication_classes = [JWTAuthentication]  # Autenticacion
    permission_classes = [IsAuthenticatedUser]  # Permisos
    queryset = Comment.objects.all()

    def get_object(self):
        return self.queryset.get(id=self.kwargs['pk'])