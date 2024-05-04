import string
import random
from datetime import datetime, timedelta
from rest_framework_simplejwt.authentication import JWTAuthentication
from codeia.models import Subscription, Plan
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import generics
from rest_framework import permissions
from codeia.permissions import IsAdminUser
from .serializers import (
    SubscriptionAdminSerializers,
    GenerateSubscriptionSerializer,
    SubscribeSerializer
)

class ListSubscriptionView(generics.ListAPIView):
    serializer_class = SubscriptionAdminSerializers
    authentication_classes = [JWTAuthentication]  # Autenticacion
    permission_classes = [IsAdminUser]  # Permisos
    queryset = Subscription.objects.all().order_by('id')

class GetSubscriptionView(generics.RetrieveAPIView):
    serializer_class = SubscriptionAdminSerializers
    authentication_classes = [JWTAuthentication]  # Autenticacion
    permission_classes = [IsAdminUser]  # Permisos
    queryset = Subscription.objects.all()

    def get_queryset(self):
        return self.queryset.filter(id=self.kwargs['pk'])
    
class GetSubscriptionUserView(generics.RetrieveAPIView):
    serializer_class = SubscriptionAdminSerializers
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user_subscriptions = Subscription.objects.filter(user_id=self.request.user.id, status='active')
        if len(user_subscriptions) == 0:
            return Response({'status': False, 'message': 'No subscription found'})
        
        user_subscriptions = user_subscriptions[0]
        return Response(SubscriptionAdminSerializers(user_subscriptions).data)

class GenerateSubscriptionView(generics.CreateAPIView):
    serializer_class = GenerateSubscriptionSerializer
    authentication_classes = [JWTAuthentication]  # Autenticacion
    permission_classes = [IsAdminUser]  # Permisos

    @staticmethod
    def generar_codigo():
        caracteres = string.ascii_letters + string.digits
        codigo = ''.join(random.choice(caracteres) for _ in range(16))
        return codigo.upper()

    def post(self, request):
        serializer = GenerateSubscriptionSerializer(data=request.data)
        if serializer.is_valid():

            months_duration = serializer.validated_data['months_duration']
            id_plan = serializer.validated_data['id_plan']

            if months_duration < 1:
                return Response({'status': 'error', 'message': 'Invalid months duration'})
            plan = Plan.objects.filter(id=id_plan)

            if len(plan) == 0:
                return Response({'status': 'error', 'message': 'Invalid plan'})
            
            subscription = Subscription.objects.create(months_duration=months_duration,
                id_plan=id_plan, is_activated=False, activation_code=self.generar_codigo())
            return Response({'status': 'success', 'code': subscription.activation_code})
        return Response(serializer.errors)
    
class SubscribeView(generics.CreateAPIView):
    serializer_class = SubscribeSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    def fecha_en_n_meses(n_meses):
        fecha_actual = datetime.now()
        fecha_futura = fecha_actual + timedelta(days=n_meses * 30)
        return fecha_futura

    def post(self, request):
        serializer = SubscribeSerializer(data=request.data)
        if serializer.is_valid():
            code = serializer.validated_data['code']
            subscription = Subscription.objects.filter(activation_code=code)
            if len(subscription) == 0:
                return Response({'status': 'error', 'message': 'Invalid code'})
            
            subscription = subscription[0]
            if subscription.is_activated:
                return Response({'status': 'error', 'message': 'Code already used'})
            
            user_subscriptions = Subscription.objects.filter(user_id=self.request.user.id, status='active')
            if len(user_subscriptions) > 0:
                user_subscriptions = user_subscriptions[0]
                user_subscriptions.status = 'inactive'
                user_subscriptions.save()

            subscription.is_activated = True
            subscription.user_id = self.request.user.id
            subscription.due_date = self.fecha_en_n_meses(subscription.months_duration)
            subscription.status = 'active'
            subscription.save()

            return Response({'status': 'success'})
        return Response(serializer.errors)

class UpdateSubscriptionView(generics.UpdateAPIView):
    serializer_class = SubscriptionAdminSerializers
    authentication_classes = [JWTAuthentication]  # Autenticacion
    permission_classes = [IsAdminUser]  # Permisos
    queryset = Subscription.objects.all()

    def get_object(self):
        return self.queryset.get(id=self.kwargs['pk'])

class DeleteSubscriptionView(generics.DestroyAPIView):
    serializer_class = SubscriptionAdminSerializers
    authentication_classes = [JWTAuthentication]  # Autenticacion
    permission_classes = [IsAdminUser]  # Permisos
    queryset = Subscription.objects.all()

    def get_object(self):
        return self.queryset.get(id=self.kwargs['pk'])