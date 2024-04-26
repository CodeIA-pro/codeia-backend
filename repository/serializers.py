from rest_framework import serializers
from codeia.models import Repository
from project.serializers import ListProjectSerializer

class RepositorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Repository
        fields = ['id', 'title', 'description', 'user_id']
        read_only_fields = ['id','user_id']

    def validate_title(self, value):
        # Reemplaza todos los espacios con guiones
        return value.replace(' ', '-')

class ListRepositorySerializer(serializers.ModelSerializer):
    #projects = ListProjectSerializer(many=True)
    project_count = serializers.SerializerMethodField()
    class Meta:
        model = Repository
        fields = ['id', 'title', 'description', 'created_at','project_count']
        read_only_fields = ['id', 'project_count']

    def get_project_count(self, obj):
        return obj.projects.all().count()
        
        #def get_projects(self, obj):
           #projects_repo = obj.projects.all().order_by('id')
            #return ListProjectSerializer(projects_repo).data
        
# Generate Connection Serializer
class BasicRepositorySerializer(serializers.Serializer):
    status = serializers.BooleanField()


# Generate Connection Serializer
class GenerateRepositorySerializer(serializers.Serializer):
    pass
