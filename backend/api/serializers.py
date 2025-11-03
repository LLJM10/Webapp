from rest_framework import serializers
from django.utils import timezone
from .models import Todo, Pitch, Event   # dein Model

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


class EventSerializer(serializers.ModelSerializer):
    """
    Serializer for Event model.
    owner is read-only and set automatically in the viewset.
    Includes validation for required fields.
    """
    owner = serializers.CharField(source='owner.username', read_only=True)

    class Meta:
        model = Event
        fields = [
            'id', 'owner', 'name', 'topic', 'location', 'duration',
            'date', 'link', 'description', 'img', 'host', 'is_public',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'owner', 'created_at', 'updated_at']

    def validate_name(self, value):
        """Event name must be at least 3 characters"""
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Event-Name muss mindestens 3 Zeichen haben.")
        return value

    def validate_duration(self, value):
        """Duration must be positive and max 8 hours (480 min)"""
        if value <= 0:
            raise serializers.ValidationError("Dauer muss größer als 0 sein.")
        if value > 480:
            raise serializers.ValidationError("Event kann maximal 8 Stunden (480 Min) dauern.")
        return value

    def validate_date(self, value):
        """Event date must be in the future"""
        if value < timezone.now():
            raise serializers.ValidationError("Event-Datum muss in der Zukunft liegen.")
        return value

    def validate_img(self, value):
        """Check if URL is valid (optional)"""
        if value and not (value.startswith('http://') or value.startswith('https://')):
            raise serializers.ValidationError("Bild-URL muss mit http:// oder https:// beginnen.")
        return value

    def validate(self, data):
        """Cross-field validation"""
        # Set host to username if not provided and event is public
        if data.get('is_public', True) and not data.get('host'):
            data['host'] = self.context['request'].user.username
        return data
