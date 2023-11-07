from rest_framework import serializers
from codeia.models import FAQ

class FAQSerializers(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ['id', 'question', 'answer']
        read_only_fields = ['id',]