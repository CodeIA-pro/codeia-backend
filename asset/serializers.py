from rest_framework import serializers
from codeia.models import Asset
    
class ListAssetSerializer(serializers.ModelSerializer):
    subsection = serializers.SerializerMethodField()
    star_average = serializers.SerializerMethodField()
    start_quantity = serializers.SerializerMethodField()
    class Meta:
        model = Asset
        fields = ['id', 'version', 'titulo', 'description', 'more_description', 'depth', 
                  'is_father', 'father_id', 'subsection', 'privacy', 'star_average', 'start_quantity', 'theme',]
        read_only_fields = ['id', 'created_at']
        
    def get_subsection(self, obj):
        subsection_asset = obj.subsection.all().order_by('id')
        return ListAssetSerializer(subsection_asset, many=True).data
    
    def get_star_average(self, obj):
        if len(obj.stars) == 0:
            return 0
        return round(sum([star['value'] for star in obj.stars]) / len(obj.stars))
    
    def get_start_quantity(self, obj):
        return len(obj.stars)

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

class MarkdownAssetSerializer(serializers.Serializer):
    asset_id = serializers.IntegerField()
    markdownText = serializers.CharField()


class DownloadAssetSerializer(serializers.Serializer):
    project_id = serializers.IntegerField()
    asset_id = serializers.IntegerField()

class PrivacyAssetInfoSerializer(serializers.Serializer):
    status = serializers.CharField()
    privacy = serializers.CharField()

class StarSerializer(serializers.Serializer):
    star = serializers.IntegerField()
    asset_id = serializers.IntegerField()

# Error Serializer
class ErrorSerializer(serializers.Serializer):
    error = serializers.CharField()