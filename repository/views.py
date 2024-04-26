from rest_framework_simplejwt.authentication import JWTAuthentication
from codeia.models import Repository, Project, User
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics, permissions,status
from django.shortcuts import get_object_or_404 
from project.serializers import ListProjectSerializer
from .serializers import (
    RepositorySerializers,
    ListRepositorySerializer,
    GenerateRepositorySerializer,
    BasicRepositorySerializer,
)


class ListRepositoryView(generics.ListAPIView):
    serializer_class = ListRepositorySerializer
    authentication_classes = [JWTAuthentication]  # Autenticacion
    permission_classes = [permissions.IsAuthenticated]  # Permisos
    queryset = Repository.objects.all().order_by('id')

    def get_queryset(self):
        return self.queryset.filter(user_id=self.request.user.id)
    
class ListRepositoryToProjectView(generics.ListAPIView):
    serializer_class = ListProjectSerializer
    authentication_classes = [JWTAuthentication]  # Autenticacion
    permission_classes = [permissions.IsAuthenticated]  # Permisos
    queryset = Project.objects.all().order_by('id')

    def get_queryset(self):
        repository = get_object_or_404(Repository, title=self.kwargs['name'], user_id=self.request.user.id)
        return repository.projects.all()
    
class RetrieveRepositoryNameView(generics.RetrieveAPIView):
    serializer_class = BasicRepositorySerializer
    authentication_classes = [JWTAuthentication]  # Autenticacion
    permission_classes = [permissions.IsAuthenticated]  # Permisos
    queryset = Repository.objects.all()

    def get_object(self):
        repo_name = self.kwargs['name']
        repo = Repository.objects.filter(title=repo_name, user_id=self.request.user.id).first()
        if not repo:
            return Response({'status': False})
        return Response({'status': True})
    
    def retrieve(self, request, *args, **kwargs):
        # Aquí se invoca get_object y se maneja la respuesta.
        return self.get_object()
    
class RetrieveRepositoryNameInformationView(generics.ListAPIView):
    serializer_class = ListRepositorySerializer
    authentication_classes = [JWTAuthentication]  # Autenticación
    permission_classes = [permissions.IsAuthenticated]  # Permisos
    queryset = Repository.objects.all()

    def get_queryset(self):
        name = self.kwargs['name']
        return self.queryset.filter(title=name, user_id=self.request.user.id)
    
class CreateRepositoryView(generics.CreateAPIView):
    serializer_class = RepositorySerializers
    authentication_classes = [JWTAuthentication]  # Autenticacion
    permission_classes = [permissions.IsAuthenticated]  # Permisos
    queryset = Repository.objects.all()

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class UpdateRepositoryView(generics.UpdateAPIView):
    serializer_class = RepositorySerializers
    authentication_classes = [JWTAuthentication]  # Autenticacion
    permission_classes = [permissions.IsAuthenticated]  # Permisos
    queryset = Repository.objects.all()

    def get_object(self):
        return self.queryset.get(id=self.kwargs['pk'], user_id=self.request.user.id)
    

class AddProjectToRepositoryView(generics.UpdateAPIView):
    serializer_class = GenerateRepositorySerializer
    authentication_classes = [JWTAuthentication]  # Autenticación
    permission_classes = [permissions.IsAuthenticated]  # Permisos
    queryset = Repository.objects.all()
    allowed_methods = ['PUT']
    
    def get_object(self):
        repo_id = self.kwargs['pk']
        repo = get_object_or_404(Repository, id=repo_id, user_id=self.request.user.id)
        return self.queryset.get(id=repo.id)

    def update(self, request, *args, **kwargs):
        repository = self.get_object()
        project_id = kwargs.get('project_id')  # Obtener el project_id de los kwargs
        project = get_object_or_404(Project, id=project_id)  # Obtener el objeto Project
        user = get_object_or_404(User, id=self.request.user.id)
        if not project in user.projects.all():
            raise PermissionDenied("Project not found")

        repository.projects.add(project)
        repository.save()

        serializer = self.get_serializer(data={'status': True})
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data)
    
class ChangeRepositoryProjectView(generics.UpdateAPIView):
    serializer_class = GenerateRepositorySerializer
    authentication_classes = [JWTAuthentication]  # Autenticación
    permission_classes = [permissions.IsAuthenticated]  # Permisos
    queryset = Repository.objects.all()
    allowed_methods = ['PUT']

    def get_object(self):
        return self.queryset.get(id=self.kwargs['pk'])

    def update(self, request, *args, **kwargs):
        repository = self.get_object()
        change_repo_id = kwargs.get('change_repo_id')
        project_id = kwargs.get('project_id')  # Obtener el project_id de los kwargs
        project = get_object_or_404(Project, id=project_id)  # Obtener el objeto Project
        repository.projects.remove(project)
        repository.save()

        change_repo = get_object_or_404(Repository, id=change_repo_id)
        change_repo.projects.add(project)
        change_repo.save()

        serializer = self.get_serializer(data={'status': True})
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data)