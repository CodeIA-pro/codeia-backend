from rest_framework import serializers
from codeia.models import Plan

class PlanSerializers(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ['id', 'name', 'description']
        read_only_fields = ['id', 'created_at']