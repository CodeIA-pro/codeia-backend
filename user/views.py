from rest_framework import (
    generics,
    permissions,
    status,
) 
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from rest_framework.pagination import PageNumberPagination
from codeia.permissions import IsAdminUser
from codeia.models import User
from email_system.send_email import email_verify, generate_code
from .serializers import (
    MyTokenObtainPairSerializer,
    MyTokenTwoFASerializer,
    UserSerializer,
    RegisterSerializer,
    UserSerializerAdmin,
    CheckSerializer,
    UserPassSerializer,
    UserChangeSerializer,
    TokenObtainPairSerializer,
    UserSerializerAdminUpdate,
)

class CustomPagination(PageNumberPagination):
    page_size = 10  # Establece el tamaño de página que desees
    page_size_query_param = 'page_size'
    max_page_size = 100

class LoginView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    permission_classes = [permissions.AllowAny]

class AdminLoginView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer
    permission_classes = [permissions.AllowAny]

class LoginTwoFAView(TokenObtainPairView):
    serializer_class = MyTokenTwoFASerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        # print(response.data)
        # return Response({'message': 'User already exists', 'status': True})
        return response

class CreateUserView(generics.CreateAPIView):  
    permission_classes = [permissions.AllowAny]  
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        return user

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        email = request.data.get('email')
        user = User.objects.filter(email=email)
        if len(user) > 0:
            return Response({'message': 'User already exists', 'status': True})
        serializer.is_valid(raise_exception=False)
        password = request.data.get('password')
        serializer.validated_data['password'] = make_password(password)
        code = generate_code()
        user = self.perform_create(serializer)
        user.verification_code = code
        user.save()

        headers = self.get_success_headers(serializer.data)
        email_verify(serializer.data['email'], serializer.data['name'] + " " + serializer.data['surname'], code) 
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
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        if 'email' in request.data:
            email = request.data['email']
            user = User.objects.filter(email=email)
            if len(user) > 0:
                return Response({'message': 'User already exists', 'status': True})

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
    
class CheckCodeView(generics.UpdateAPIView):
    """Manage the authenticated user."""
    serializer_class = CheckSerializer
    permission_classes = [permissions.AllowAny]
    allowed_methods = ['PUT']

    def get_object(self):
        serializer = self.get_serializer(data=self.request.data)

    def update(self, request, *args, **kwargs):
        code = request.data.get('code')
        user = get_object_or_404(User, verification_code=code)
        user.is_unverified = False
        user.save()
        return Response({'status': True})

class TwoFactorView(generics.CreateAPIView):
    serializer_class = UserPassSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = get_object_or_404(User, id=self.request.user.id)
        user.two_factor = not user.two_factor
        user.save()
        return Response({'status': 'success'})
"""  
Actualizar contraseña
"""
class ChangePasswordView(generics.CreateAPIView):
    serializer_class = UserChangeSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = UserChangeSerializer(data=request.data)
        if serializer.is_valid():
            password = serializer.validated_data['password']
            new_password = serializer.validated_data['new_password']
            user = get_object_or_404(User, id=self.request.user.id)
            if user.check_password(password):
                user.set_password(new_password)
                user.save()
                return Response({'message': 'Password changed successfully', 'status': True})
            else:
                return Response({'message': 'Password incorrect', 'status': False})

        return Response(serializer.errors)

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