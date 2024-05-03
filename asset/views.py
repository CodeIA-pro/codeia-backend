from app import settings
import uuid
from rest_framework.response import Response
from rest_framework import generics, permissions,status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import PermissionDenied, ValidationError
from django.shortcuts import get_object_or_404 
from codeia.models import Asset, Project, Star, User
from django.forms.models import model_to_dict
from rest_framework.pagination import PageNumberPagination
from codeia.permissions import IsAuthenticatedUser
from .serializers import (
    AssetSerializer,
    ListAssetSerializer,
    ChangeAssetSerializer,
    PrivacyAssetSerializer,
    PrivacyAssetInfoSerializer,
    StarSerializer,
    ErrorSerializer,
)

class CustomPagination(PageNumberPagination):
    page_size = 10  # Establece el tamaño de página que desees
    page_size_query_param = 'page_size'
    max_page_size = 100


"""
Listado de assets
"""
class ListAssetView(generics.ListAPIView):
    serializer_class = ListAssetSerializer
    permission_classes = [permissions.AllowAny] 
    queryset = Asset.objects.filter(depth=0).order_by('id')

""" 
Listar Asset por version y projecto
"""
class ListAssetByVersionView(generics.ListAPIView):
    serializer_class = ListAssetSerializer
    authentication_classes = [JWTAuthentication]  # Autenticacion
    permission_classes = [permissions.IsAuthenticated]  # Permisos
    queryset = Asset.objects.all()

    def get_queryset(self):
        version = self.kwargs['version']
        title = self.kwargs['title']
        user_repo = self.kwargs['user_repo']
        project = get_object_or_404(Project, title=title, user_repo=user_repo)
        user = get_object_or_404(User, pk=self.request.user.id)
        if not project in user.projects.all():
            raise PermissionDenied({'status': 'Not found'})
        return Asset.objects.filter(version=version, project_id=project.id, depth=0).order_by('id')
    
""" 
Listar Asset por version y projecto y url
"""
class ListAssetByVersionURLView(generics.ListAPIView):
    serializer_class = ListAssetSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Asset.objects.all()

    def get_queryset(self):
        version = self.kwargs['url_version']
        return Asset.objects.filter(url=version, depth=0).order_by('id')

"""  
Crear asset
"""
class CreateAssetView(generics.CreateAPIView):
    serializer_class = AssetSerializer
    permission_classes = [permissions.AllowAny]

    def get_next_version(self, project_id):
        last_asset = Asset.objects.filter(depth=0, project_id=project_id).last()
        if not last_asset:
            return '1.0.0'
        
        major, minor, patch = map(int, last_asset.version.split('.'))
        if patch < 10:
            patch += 1
        else:
            patch = 0
            major += 1
        
        return f"{major}.{minor}.{patch}"

    def perform_create(self, serializer):
        project_id = self.kwargs['project_id']
        project = get_object_or_404(Project, pk=project_id)
        data = dict(serializer.validated_data)
        data['project_id'] = project.id
        data['version'] = self.get_next_version(project.id)
        new_asset = Asset.objects.create(**data)
        project.assets.add(new_asset)
        project.last_version = new_asset.version
        project.save(update_fields=['last_version'])
        return Response({'message': 'Product created successfully'}, status=status.HTTP_201_CREATED)

"""
Cambiar privacidad de asset
"""
class PrivacyAssetStatusView(generics.CreateAPIView):
    serializer_class = PrivacyAssetSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = PrivacyAssetSerializer(data=request.data)
        if serializer.is_valid():
            project_id = serializer.validated_data['project_id']
            asset_parent = serializer.validated_data['asset_id']
            privacy = serializer.validated_data['privacy']
            # Validar que el proyecto exista
            project = get_object_or_404(Project, id=project_id)
            user = get_object_or_404(User, id=self.request.user.id)
            if not project in user.projects.all():
                raise PermissionDenied("Project not found")
            
            asset_father = get_object_or_404(Asset, id=asset_parent, project_id=project_id)
            # generar uuid
            link = uuid.uuid4()
            asset_father.privacy = privacy
            if privacy == 'public':
                asset_father.url = link
            else:
                asset_father.url = ''
            asset_father.url = link
            asset_father.save()

            return Response({
                'status': 'success',
                'link': link ,
                'project_id': project.id,
                'asset_id': asset_father.id,
                'privacy': privacy 
                })
        return Response(serializer.errors)
    
"""
Consular privacidad de asset
"""
class PrivacyAssetStatusInfoView(generics.RetrieveAPIView):
    serializer_class = PrivacyAssetInfoSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, project_id, asset_id):
        # Validar que el proyecto exista
        project = get_object_or_404(Project, id=project_id)
        user = get_object_or_404(User, id=self.request.user.id)
        if not project in user.projects.all():
            raise PermissionDenied("Project not found")
        asset_father = get_object_or_404(Asset, id=asset_id, project_id=project_id)
        
        return Response({
            'status': 'success',
            'privacy': asset_father.privacy,
            'link': asset_father.url,
        })

"""
Crear subsección
"""
class CreatesSubSectionView(generics.CreateAPIView):
    serializer_class = AssetSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        pk = self.kwargs['pk']
        asset = get_object_or_404(Asset, pk=pk)
        data = dict(serializer.validated_data)
        data['depth'] = asset.depth + 1
        data['father_id'] = asset.id
        data['version'] = asset.version
        data['project_id'] = asset.project_id
        new_related_product = Asset.objects.create(**data)
        asset.subsection.add(new_related_product)
        asset.is_father = True
        asset.save(update_fields=['is_father'])

        return Response({'message': 'Product subsection added successfully'}, status=status.HTTP_201_CREATED)

"""  
Agregar estrellas
"""
class StarAssetView(generics.CreateAPIView):
    serializer_class = StarSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = StarSerializer(data=request.data)
        if serializer.is_valid():
            star_value = serializer.validated_data['star']
            asset_id = serializer.validated_data['asset_id']
            asset = get_object_or_404(Asset, id=asset_id, depth=0)
            star_obj = Star(value=star_value)
            asset.stars.append(model_to_dict(star_obj))
            asset.save()
            return Response({'status': 'success'})
        return Response(serializer.errors)

"""
Update asset
"""
class UpdateAssetView(generics.UpdateAPIView):
    serializer_class = AssetSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Asset.objects.all()

    def perform_update(self, serializer):
        pk = self.kwargs['pk']
        asset = get_object_or_404(Asset, pk=pk)
        data = dict(serializer.validated_data)
        serializer.save(**data)
        return Response({'message': 'Product updated successfully'}, status=status.HTTP_200_OK)

"""
Delete asset
"""
class DeleteAssetView(generics.DestroyAPIView):
    serializer_class = ChangeAssetSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Asset.objects.all()

    def delete(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        instance = get_object_or_404(Asset, pk=pk)
        self.recursive_delete(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def recursive_delete(self, instance):
        father_instance = None
        children = Asset.objects.filter(father_id=instance.id)
        for child in children:
            self.recursive_delete(child)
        if instance.father_id:
            father_instance = Asset.objects.get(id=instance.father_id)
        instance.delete()
        if father_instance and not Asset.objects.filter(father_id=father_instance.id):
            father_instance.is_father = False
            father_instance.save()