from rest_framework import serializers
from codeia.models import Asset
    
class ListAssetSerializer(serializers.ModelSerializer):
    subsection = serializers.SerializerMethodField()
    class Meta:
        model = Asset
        fields = ['id', 'version', 'titulo', 'description', 'more_description', 'depth', 
                  'is_father', 'father_id', 'subsection', 'privacy',]
        read_only_fields = ['id', 'created_at']
        
    def get_subsection(self, obj):
        subsection_asset = obj.subsection.all().order_by('id')
        return ListAssetSerializer(subsection_asset, many=True).data

class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = ['id', 'titulo', 'description', 'more_description', 'url']
        read_only_fields = ['id', 'created_at']
    
class ChangeAssetSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Asset
        fields = []
        read_only_fields = ['id', 'version', 'titulo', 'description', 'more_description', 'depth', 'url', 
                            'is_father', 'father_id', 'subsection']

# Error Serializer
class PrivacyAssetSerializer(serializers.Serializer):
    project_id = serializers.IntegerField()
    asset_id = serializers.IntegerField()
    privacy = serializers.CharField()

class PrivacyAssetInfoSerializer(serializers.Serializer):
    status = serializers.CharField()
    privacy = serializers.CharField()


# Error Serializer
class ErrorSerializer(serializers.Serializer):
    error = serializers.CharField()