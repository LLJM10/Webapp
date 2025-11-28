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
    
    # FileFields explizit deklarieren für bessere Kontrolle
    img = serializers.ImageField(required=False, allow_null=True)
    pitch_deck = serializers.FileField(required=False, allow_null=True)
    business_plan = serializers.FileField(required=False, allow_null=True)
    financial_report = serializers.FileField(required=False, allow_null=True)

    class Meta:
        model = Pitch
        fields = [
            'id', 'owner', 'title', 'sector', 'stage', 'goal', 
            'equity', 'desc', 'img', 'valuation', 'is_public',
            'pitch_deck', 'business_plan', 'financial_report',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'owner', 'created_at', 'updated_at']
    
    def validate_img(self, value):
        """Validate pitch image file"""
        if value and hasattr(value, 'size'):
            if value.size > 5242880:  # 5MB
                raise serializers.ValidationError("Bild zu groß. Maximum: 5MB")
        return value
    
    def validate_pitch_deck(self, value):
        """Validate pitch deck PDF file"""
        if value and not value.name.endswith('.pdf'):
            raise serializers.ValidationError("Nur PDF-Dateien erlaubt.")
        if value and value.size > 10485760:  # 10MB
            raise serializers.ValidationError("Datei zu groß. Maximum: 10MB")
        return value
    
    def validate_business_plan(self, value):
        """Validate business plan PDF file"""
        if value and not value.name.endswith('.pdf'):
            raise serializers.ValidationError("Nur PDF-Dateien erlaubt.")
        if value and value.size > 10485760:
            raise serializers.ValidationError("Datei zu groß. Maximum: 10MB")
        return value
    
    def validate_financial_report(self, value):
        """Validate financial report PDF file"""
        if value and not value.name.endswith('.pdf'):
            raise serializers.ValidationError("Nur PDF-Dateien erlaubt.")
        if value and value.size > 10485760:
            raise serializers.ValidationError("Datei zu groß. Maximum: 10MB")
        return value


class EventSerializer(serializers.ModelSerializer):
    """
    Serializer for Event model.
    owner is read-only and set automatically in the viewset.
    Includes validation for required fields.
    """
    owner = serializers.CharField(source='owner.username', read_only=True)
    img = serializers.ImageField(required=False, allow_null=True)

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
        """Validate event image file"""
        if value and hasattr(value, 'size'):
            if value.size > 5242880:  # 5MB
                raise serializers.ValidationError("Bild zu groß. Maximum: 5MB")
        return value

    def validate(self, data):
        """Cross-field validation"""
        # Set host to username if not provided and event is public
        if data.get('is_public', True) and not data.get('host'):
            data['host'] = self.context['request'].user.username
        return data
