from rest_framework import serializers
from codeia.models import TypeComment

class TypeCommentSerializers(serializers.ModelSerializer):
    class Meta:
        model = TypeComment
        fields = ['id', 'description']
        read_only_fields = ['id',]