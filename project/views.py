import os
import re
from rest_framework.response import Response
from rest_framework import generics, permissions,status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import PermissionDenied, ValidationError
from django.shortcuts import get_object_or_404 
from codeia.models import Project, User, Asset
from rest_framework.pagination import PageNumberPagination
from codeia.permissions import IsAuthenticatedUser
from asset.serializers import AssetSerializer
from .serializers import (
    ProjectSerializer,
    ListProjectSerializer,
    GetProjectSerializer,
    ChangeProjectSerializer,
    GenerateConnectionSerializer,
    ErrorSerializer,
)
from datetime import datetime
import requests
import base64
import json
from urllib.parse import urlparse, parse_qs

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
    serializer_class = GetProjectSerializer
    authentication_classes = [JWTAuthentication]  # Autenticacion
    permission_classes = [permissions.IsAuthenticated]  # Permisos
    queryset = Project.objects.all()

    def get_object(self):
        project = self.kwargs['project']
        owner = self.kwargs['owner'] 
        project = get_object_or_404(Project, user_repo=owner, title=project)
        user = get_object_or_404(User, id=self.request.user.id)
        if not project in user.projects.all():
            raise PermissionDenied("Project not found")
        return project

"""
Generar Guia de referencia para un proyecto
"""
class GenerateGuideView(generics.RetrieveAPIView):
    serializer_class = GenerateConnectionSerializer
    authentication_classes = [JWTAuthentication]  # Autenticacion
    permission_classes = [permissions.IsAuthenticated]
    
    @staticmethod
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

    def retrieve(self, request, *args, **kwargs):
        project_id = self.kwargs['pk']
        user = get_object_or_404(User, id=self.request.user.id)
        project = get_object_or_404(Project, pk=project_id)
        if not project in user.projects.all():
            raise PermissionDenied("Project not found")
        # Asumiendo que tienes una función para obtener el contenido del repo
        repo_content = project.information + '/n' + 'endpoints' + '/n' + project.urls
        # Creando projecto raiz
        next_version = self.get_next_version(self, project_id)
        sha = ''
        html_url = ''
        headers = {'Authorization': f'token {user.token_repo}'}
        response_github =requests.get( f"https://api.github.com/repos/{project.user_repo}/{project.title}/commits/{project.branch}", headers=headers)
        if response_github.status_code == 200:
            data = response_github.json()
            sha = data['sha'][:8]
            html_url = data['html_url']
        else:
            project.is_Loading = False
            project.message_failed = 'Error fetching repo tree'
            project.save()
            return Response({'status': 'Error fetching repo tree'})

        root_asset = Asset.objects.create(
            version=next_version, 
            titulo=project.title, 
            is_father=True, 
            father_id=None, 
            is_Loading=True, 
            project_id=project.id,
            short_sha=sha,
            url_commit=html_url)
        
        project.assets.add(root_asset)
        project.is_Loading = True
        project.save()
        secciones = [
            "Introducción",
            "Autenticación y Autorización",
            "Descripción General",
            "Endpoints",
            "Recomendaciones de Seguridad"
        ]
        # Crear activos de nivel 1
        print('Entrando a modelo')
        for section in secciones:
            guide_content = self.generate_text_with_gpt3(project, root_asset, repo_content, section, project.title)
            self.create_subsection(root_asset, section, guide_content)
        project.last_version = next_version
        project.latest_build = datetime.now()
        project.is_Loading = False
        root_asset.is_Loading = False
        root_asset.save(update_fields=['is_Loading'])
        project.save()
        return Response({'status': 'success'}, status=status.HTTP_200_OK)
    
    @staticmethod
    def create_subsection(parent_asset, title, description):
        # Lógica para crear una subsección
        asset = get_object_or_404(Asset, pk=parent_asset.id)
        data = {
            'titulo': title,
            'description': description,
            'depth': parent_asset.depth + 1,
            'father_id': parent_asset.id,
            'project_id': parent_asset.project_id,
            'version': parent_asset.version,
        }
        new = Asset.objects.create(**data)
        asset.subsection.add(new)
        asset.save()

    @staticmethod
    def generate_text_with_gpt3(project, root_asset, repo_content, section_title, user):
        api_key = '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'  # clave
        prompt = f"Genera directamente el contenido util para una sección titulada '{section_title}' basado en la siguiente información del proyecto Django Rest Framework:\n\n{repo_content}\n"

        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
        }

        data = {
            'model': 'gpt-4',
            'messages': [
                {
                    'role': 'system',
                    'content': 'Eres un asistente que crea contenido util y específico para secciones de documentación técnica.'
                },
                {
                    'role': 'user',
                    'content': prompt
                }
            ]
        }

        response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)
        print('Entrando a modelo')
        if response.status_code == 200:
            print(response.json()['choices'][0]['message']['content'])
            return response.json()['choices'][0]['message']['content']
        else:
            print('Error')
            print(response)
            project.is_Loading = False
            project.save()
            root_asset.is_Loading = False
            root_asset.to_failed = True
            root_asset.message_failed = 'Unexpected error in the generation system, please contact the support team'
            root_asset.save()
            raise Exception("Error in OpenAI API call", response.text)

"""
Generar Conexion a un proyecto de github
"""
class GenerateConnectionGitHubView(generics.RetrieveAPIView):
    serializer_class = GenerateConnectionSerializer
    authentication_classes = [JWTAuthentication]  # Autenticacion
    permission_classes = [permissions.IsAuthenticated]  # Permisos

    def extract_owner_repo(self, code):
        CLIENT_ID = '60cff6eabecd0033117d'
        CLIENT_SECRET = '77fb4e49418657684bc45f66f912433812254f58'
        params = "?client_id=" + CLIENT_ID + "&client_secret=" + CLIENT_SECRET + "&code=" + code
        url = "https://github.com/login/oauth/access_token" + params
        response = requests.post(url)
        if response.status_code == 200:
            if 'bad_verification_code' in response.text:
                raise PermissionDenied("Error in GitHub API")
            access_token = parse_qs(response.text)['access_token'][0]
            headers = {'Authorization': f'token {access_token}'}
            response = requests.get('https://api.github.com/user', headers=headers)
            if response.status_code == 200:
                user = get_object_or_404(User, id=self.request.user.id)
                user.token_repo = access_token
                user.repo_login = True
                user.save(update_fields=['token_repo', 'repo_login'])
                print(response.text)
                return "success"
            else:
                raise PermissionDenied("Error in GitHub API")

    def get_object(self):
        code = self.kwargs['code']
        response = self.extract_owner_repo(code)  # Usando la función independiente
        return Response({'status': 'success'})

    def retrieve(self, request, *args, **kwargs):
        # Aquí se invoca get_object y se maneja la respuesta.
        return self.get_object()    

"""
Generar Conexion a un proyecto (deprecated)
"""
class GenerateConnectionView(generics.RetrieveAPIView):
    serializer_class = GenerateConnectionSerializer
    authentication_classes = [JWTAuthentication]  # Autenticacion
    permission_classes = [permissions.IsAuthenticated]  # Permisos

    @staticmethod
    def extract_owner_repo(github_url):
        parsed_url = urlparse(github_url)
        path_parts = parsed_url.path.strip("/").split("/")
        if len(path_parts) >= 2:
            owner = path_parts[0]
            repo = path_parts[1]
            return owner, repo
        else:
            raise PermissionDenied("URL no válida. No se pudo extraer el propietario y el nombre del repositorio.")
        
    def get_object(self):
        id = self.kwargs['pk']
        path = "app/settings.py"
        project = get_object_or_404(Project, pk=id)
        owner, repo = self.extract_owner_repo(project.url_repo)  # Usando la función independiente
        url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}?ref={project.branch}"
        response = requests.get(url)
        if response.status_code == 200:
            content_info = response.json()
            content = base64.b64decode(content_info['content'])
            #return Response({'status': 'success', 'data': content.decode('utf-8')})
            project.information = content.decode('utf-8') 
            project.save(update_fields=['information'])
            return Response({'status': 'success', 'data': content.decode('utf-8')})
        else:
            # Usar el serializador de error para proporcionar una respuesta adecuada
            error_serializer = ErrorSerializer(data={'error': response.text})
            if error_serializer.is_valid():
                return Response(error_serializer.data, status=response.status_code)
            else:
                return Response({'error': 'Error desconocido'}, status=response.status_code)

    def retrieve(self, request, *args, **kwargs):
        # Aquí se invoca get_object y se maneja la respuesta.
        return self.get_object()

"""
Obtener informacion de usuario de github
"""
class RetrieveGitHubUserInfo(generics.RetrieveAPIView):
    serializer_class = GenerateConnectionSerializer
    authentication_classes = [JWTAuthentication]  # Autenticacion
    permission_classes = [permissions.IsAuthenticated]  # Permisos

    def get_object(self):
        user = get_object_or_404(User, id=self.request.user.id)
        headers = {'Authorization': f'token {user.token_repo}'}
        response = requests.get('https://api.github.com/user', headers=headers)
        if response.status_code == 200:
            return Response({'status': 'success', 'data': response.json()})
        else:
            user = get_object_or_404(User, id=self.request.user.id)
            user.repo_login = False
            user.save(update_fields=['repo_login'])
            return Response({'status': 'Expired token'}, status=response.status_code) 

    def retrieve(self, request, *args, **kwargs):
        # Aquí se invoca get_object y se maneja la respuesta.
        return self.get_object()

"""
Obtener repositorios de usuario de github
"""
class RetrieveGitHubUserRepos(generics.RetrieveAPIView):
    serializer_class = GenerateConnectionSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        user = get_object_or_404(User, id=self.request.user.id)
        headers = {'Authorization': f'token {user.token_repo}'}
        response = requests.get('https://api.github.com/user/repos?page=1&per_page=100', headers=headers)

        if response.status_code == 200:
            user_projects = user.projects.all()
            github_repos = response.json()

            for github_repo in github_repos:
                matching_project = next((proj for proj in user_projects if proj.title == github_repo.get('name')), None)
                if matching_project:
                    github_repo['isProject'] = True
                else:
                    github_repo['isProject'] = False

            return Response({'status': 'success', 'data': github_repos})
        else:
            user.repo_login = False
            user.save(update_fields=['repo_login'])
            return Response({'status': 'Expired token'}, status=response.status_code) 

    def retrieve(self, request, *args, **kwargs):
        return self.get_object()

"""
Obtener ramas de un repositorio de github
"""
class RetrieveGitHubRepoBranches(generics.RetrieveAPIView):
    serializer_class = GenerateConnectionSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        ower = self.kwargs['owner']
        repo = self.kwargs['repo']
        user = get_object_or_404(User, id=self.request.user.id)
        headers = {'Authorization': f'token {user.token_repo}'}
        response = requests.get('https://api.github.com/repos/{}/{}/branches'.format(ower, repo), headers=headers)

        if response.status_code == 200:
            return Response({'status': 'success', 'data': response.json()})
        else:
            return Response({'status': 'Not found'}, status=response.status_code)

    def retrieve(self, request, *args, **kwargs):
        return self.get_object()

"""
Obtener lenguajes de un repositorio de github
"""
class RetrieveGitHubRepoLanguages(generics.RetrieveAPIView):
    serializer_class = GenerateConnectionSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        owner = self.kwargs['owner']
        repo = self.kwargs['repo']
        user = get_object_or_404(User, id=self.request.user.id)
        headers = {'Authorization': f'token {user.token_repo}'}
        response = requests.get(f'https://api.github.com/repos/{owner}/{repo}/languages', headers=headers)

        if response.status_code == 200:
            languages = response.json()

            # Verificar si Python está presente y el diccionario de lenguajes no está vacío
            is_python_repo = 'Python' in languages and bool(languages)

            return Response({'status': 'success', 'is_python_repo': is_python_repo})
        else:
            return Response({'status': 'Not found'}, status=response.status_code)

    def retrieve(self, request, *args, **kwargs):
        return self.get_object()
    
"""  
Leer repositorio de github de un proyecto (pre-generación)
"""
class RetrieveInformationGitHubRepoView(generics.RetrieveAPIView):

    serializer_class = GenerateConnectionSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):

        id = self.kwargs['pk']
        project = get_object_or_404(Project, pk=id)
        user = get_object_or_404(User, id=self.request.user.id)
        headers = {'Authorization': f'token {user.token_repo}'}
        settings_url = None
        # Obtener el árbol de archivos del repo
        url = f"https://api.github.com/repos/{project.user_repo}/{project.title}/git/trees/{project.branch}"
        response = requests.get(url, headers=headers)
        project.is_Loading = True
        if response.status_code == 200:
            tree = response.json()['tree']

            # Buscar settings.py en cualquier parte del árbol   
            for item in tree:
                if item['type'] == 'tree':
                    subdir_url = item['url']
                    subdir_response = requests.get(subdir_url, headers=headers)
                    if subdir_response.status_code == 200:
                        subdir_tree = subdir_response.json()['tree']
                        
                        # Buscar en subdirectorio
                        for subitem in subdir_tree:
                            if subitem['path'].endswith('settings.py'):
                                settings_url = subitem['url']
                                break
                    else:
                        project.message_failed = 'Error fetching subdir tree'
                        project.is_Loading = False
                        project.save()
                        return Response({'status': 'Error fetching subdir tree'})
            
            # Uso de settings_url
            if settings_url is not None:
                # Obtener contenido de settings.py
                settings_response = requests.get(settings_url, headers=headers)
            else:
                project.is_Loading = False
                project.message_failed = 'Error finding root file "settings.py" in repo'
                project.save()
                return Response({'status': 'Error finding root file "settings.py" in repo'})
            
            if settings_response.status_code == 200:
                settings_content = base64.b64decode(settings_response.json()['content']).decode()
                match = re.search(r"PROJECT_APPS\s*=\s*\[([^\]]*)\]", settings_content, re.DOTALL)
                project_apps = []
                if match:
                    project_apps_str = match.group(1)
                    project_apps = [app.strip().strip('"').strip("'") for app in project_apps_str.split(',') if app.strip()]
                else:
                    project.is_Loading = False
                    project.message_failed = 'Error finding PROJECT_APPS in repo'
                    project.save()
                    return Response({'status': 'Error finding PROJECT_APPS in repo'})

                # Construir rutas relativas a partir de PROJECT_APPS
                print(project_apps)
                urls_content = ""
                for app in project_apps:
                    url = f"https://api.github.com/repos/{project.user_repo}/{project.title}/contents/{app}/urls.py?ref={project.branch}"
                    content = requests.get(url, headers=headers)
                    if content.status_code == 200:
                        # content
                        urls_content += base64.b64decode(content.json()['content']).decode() + '\n'


                # Guardar información obtenida   
                project.information = settings_content
                project.urls = urls_content
                project.message_failed = ''
                project.save()

                return Response({'status': 'success'})

            else:
                project.is_Loading = False
                project.save()
                return Response({'status': 'Error finding root file "settings.py" in repo'})
        else:
            project.is_Loading = False
            project.save()
            return Response({'status': 'Error fetching repo tree'})

    def retrieve(self, request, *args, **kwargs):
        return self.get_object()

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
        data['latest_build'] = None
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