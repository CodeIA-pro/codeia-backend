from rest_framework import serializers
from codeia.models import Project, Asset

class ProjectAssetSerializer(serializers.ModelSerializer):
    subsection = serializers.SerializerMethodField()
    class Meta:
        model = Asset
        fields = ['id', 'version', 'titulo', 'description', 'more_description', 'depth', 'url', 
                  'is_father', 'father_id', 'subsection', 'is_Loading', 'to_failed', 'message_failed', 'url_commit', 'short_sha']
        read_only_fields = ['id', 'created_at']

    def get_subsection(self, obj):
        subsection_asset = obj.subsection.all().order_by('id')
        return ProjectAssetSerializer(subsection_asset, many=True).data

class ListProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ['id', 'title', 'branch', 'url_repo', 'user_repo', 'latest_build', 
                  'last_version','is_Loading', 'message_failed']
        read_only_fields = ['id']

class InfoProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ['id', 'information','serializer_info', 'url_info', 'view_info', 'lang']
        read_only_fields = ['id']


class GetProjectSerializer(serializers.ModelSerializer):
    assets = ProjectAssetSerializer(many=True)
    class Meta:
        model = Project
        fields = ['id', 'title', 'branch', 'url_repo', 'user_repo', 'latest_build', 
                  'last_version', 'assets', 'is_Loading', 'message_failed']
        read_only_fields = ['id']

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title', 'branch', 'url_repo', 'user_repo', 'root']
        read_only_fields = ['id']
    
class ChangeProjectSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Project
        fields = []
        read_only_fields = ['id', 'title', 'branch', 'url_repo', 'user_repo', 'latest_build', 
                  'last_version']

# Generate Connection Serializer

class GenerateConnectionSerializer(serializers.Serializer):
    status = serializers.CharField()

class VersionSerializer(serializers.Serializer):
    status = serializers.BooleanField()

# Error Serializer
class ErrorSerializer(serializers.Serializer):
    error = serializers.CharField()