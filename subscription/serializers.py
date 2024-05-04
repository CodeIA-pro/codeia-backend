from rest_framework import serializers
from codeia.models import Subscription

class SubscriptionAdminSerializers(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['id', 'id_plan', 'user_id', 'months_duration', 'activation_code', 'status', 'is_activated', 'due_date']
        read_only_fields = ['id', 'created_at']

class SubscriptionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['id', 'id_plan', 'due_date']
        read_only_fields = ['id', 'created_at']

class GenerateSubscriptionSerializer(serializers.Serializer):
    months_duration = serializers.IntegerField()
    id_plan = serializers.IntegerField()

class SubscribeSerializer(serializers.Serializer):
    code = serializers.CharField()

class CancelSerializer(serializers.Serializer):
    pass