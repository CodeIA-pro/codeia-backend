from rest_framework import (
    generics,
    permissions,
    status,
) 
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from rest_framework.pagination import PageNumberPagination
from codeia.permissions import IsAdminUser
from codeia.models import User
from .serializers import (
    MyTokenObtainPairSerializer,
    UserSerializer,
    RegisterSerializer,
    UserSerializerAdmin,
    UserSerializerAdminUpdate,
)

class CustomPagination(PageNumberPagination):
    page_size = 10  # Establece el tamaño de página que desees
    page_size_query_param = 'page_size'
    max_page_size = 100

class LoginView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    permission_classes = [permissions.AllowAny]

class CreateUserView(generics.CreateAPIView):  
    permission_classes = [permissions.AllowAny]  
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = request.data.get('password')
        serializer.validated_data['password'] = make_password(password)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        response_data = {'message': 'User created successfully'}
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)



class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user."""
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]  # Autenticacion
    permission_classes = [permissions.IsAuthenticated]  # Permisos

    def get_object(self):
        """Retrieve and return the authenticated user."""
        return self.request.user

"""
Admin view
"""
class ListUserViewAdmin(generics.ListAPIView):
    """Manage the authenticated user."""
    serializer_class = UserSerializerAdmin
    authentication_classes = [JWTAuthentication]  # Autenticacion
    permission_classes = [IsAdminUser]  # Permisos
    pagination_class = CustomPagination
    queryset = User.objects.all().order_by('id')

class UpdateUserViewAdmin(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user."""
    serializer_class = UserSerializerAdminUpdate
    authentication_classes = [JWTAuthentication]  # Autenticacion
    permission_classes = [IsAdminUser]  # Permisos
    queryset = User.objects.all()