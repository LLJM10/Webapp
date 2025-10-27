from rest_framework import serializers
from .models import Todo, Pitch   # dein Model

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = "__all__"


class PitchSerializer(serializers.ModelSerializer):
    """
    Serializer for Pitch model.
    owner is read-only and set automatically in the viewset.
    """
    owner = serializers.CharField(source='owner.username', read_only=True)

    class Meta:
        model = Pitch
        fields = [
            'id', 'owner', 'title', 'sector', 'stage', 'goal', 
            'equity', 'desc', 'img', 'valuation', 'is_public', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'owner', 'created_at', 'updated_at']
