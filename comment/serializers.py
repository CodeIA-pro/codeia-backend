from rest_framework import serializers
from codeia.models import Comment

class ListCommentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'user', 'title', 'description', 'type_comment']
        read_only_fields = ['id', 'created_at']

class CommentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'title', 'description']
        read_only_fields = ['id', 'created_at']