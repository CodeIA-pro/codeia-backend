from rest_framework.response import Response
from rest_framework import generics, permissions,status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import PermissionDenied, ValidationError
from django.shortcuts import get_object_or_404 
from codeia.models import Project, User
from rest_framework.pagination import PageNumberPagination
from codeia.permissions import IsAuthenticatedUser
from .serializers import (
    ProjectSerializer,
    ListProjectSerializer,
    ChangeProjectSerializer,
    ErrorSerializer,
)

class CustomPagination(PageNumberPagination):
    page_size = 10  # Establece el tamaño de página que desees
    page_size_query_param = 'page_size'
    max_page_size = 100

"""
Listado de proyectos
"""
class ListProjectView(generics.ListAPIView):
    serializer_class = ListProjectSerializer
    authentication_classes = [JWTAuthentication]  # Autenticacion
    permission_classes = [permissions.IsAuthenticated]  # Permisos
    queryset = Project.objects.filter().order_by('id')

    def get_queryset(self):
        user = get_object_or_404(User, id=self.request.user.id)
        return user.projects.all().order_by('id')

"""
Listar un proyecto
"""
class RetrieveProjectView(generics.RetrieveAPIView):
    serializer_class = ListProjectSerializer
    authentication_classes = [JWTAuthentication]  # Autenticacion
    permission_classes = [permissions.IsAuthenticated]  # Permisos
    queryset = Project.objects.all()

    def get_object(self):
        id = self.kwargs['pk']
        project = get_object_or_404(Project, pk=id)
        user = get_object_or_404(User, id=self.request.user.id)
        if not project in user.projects.all():
            raise PermissionDenied("Project not found")
        return project 

"""  
Crear proyectos
"""
class CreateProjectView(generics.CreateAPIView):
    serializer_class = ProjectSerializer
    authentication_classes = [JWTAuthentication]  # Autenticacion
    permission_classes = [permissions.IsAuthenticated]  # Permisos

    def perform_create(self, serializer):
        user = get_object_or_404(User, id=self.request.user.id)
        data = dict(serializer.validated_data)
        new_asset = Project.objects.create(**data)
        user.projects.add(new_asset)
        user.save()
        return Response({'message': 'Product created successfully'}, status=status.HTTP_201_CREATED)

"""
Update proyectos
"""
class UpdateProjectView(generics.UpdateAPIView):
    serializer_class = ProjectSerializer
    authentication_classes = [JWTAuthentication]  # Autenticacion
    permission_classes = [permissions.IsAuthenticated]  # Permisos
    queryset = Project.objects.all()

    def perform_update(self, serializer):
        pk = self.kwargs['pk']
        project = get_object_or_404(Project, pk=pk)
        data = dict(serializer.validated_data)
        user = get_object_or_404(User, id=self.request.user.id)
        if not project in user.projects.all():
            raise PermissionDenied("Project not found")
        serializer.save(**data)
        return Response({'message': 'Product updated successfully'}, status=status.HTTP_200_OK)

"""
Delete proyectos
"""
class DeleteProjectView(generics.DestroyAPIView):
    serializer_class = ChangeProjectSerializer
    authentication_classes = [JWTAuthentication]  # Autenticacion
    permission_classes = [permissions.IsAuthenticated]  # Permisos
    queryset = Project.objects.all()

    def perform_destroy(self, instance):
        id = self.kwargs['pk']
        project = get_object_or_404(Project, pk=id)
        user = get_object_or_404(User, id=self.request.user.id)
        if not project in user.projects.all():
            raise PermissionDenied("Project not found")
        if project.assets.count() > 0:
            raise ValidationError("You can't delete a project with builds")
        user.projects.remove(project)
        user.save(update_fields=['projects'])
        project.delete()
        return Response({'message': 'Product deleted successfully'}, status=status.HTTP_200_OK)