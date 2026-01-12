from rest_framework import serializers
from django.utils import timezone
from .models import Todo, Pitch, Event, SavedPitch, Investment  

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = "__all__"


class PitchSerializer(serializers.ModelSerializer):
    """
    Pitch-Modell
    owner ist read-only und wird automatisch im ViewSet gesetzt.
    """
    owner = serializers.CharField(source='owner.username', read_only=True)
    
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
        """Pitch-Bild """
        if value and hasattr(value, 'size'):
            if value.size > 5242880:  # 5MB
                raise serializers.ValidationError("Bild zu groß. Maximum: 5MB")
        return value
    
    def validate_pitch_deck(self, value):
        """Pitch Deck"""
        if value and not value.name.endswith('.pdf'):
            raise serializers.ValidationError("Nur PDF-Dateien erlaubt.")
        if value and value.size > 10485760:  # 10MB
            raise serializers.ValidationError("Datei zu groß. Maximum: 10MB")
        return value
    
    def validate_business_plan(self, value):
        """Businessplan"""
        if value and not value.name.endswith('.pdf'):
            raise serializers.ValidationError("Nur PDF-Dateien erlaubt.")
        if value and value.size > 10485760:
            raise serializers.ValidationError("Datei zu groß. Maximum: 10MB")
        return value
    
    def validate_financial_report(self, value):
        """Finanzbericht PDF"""
        if value and not value.name.endswith('.pdf'):
            raise serializers.ValidationError("Nur PDF-Dateien erlaubt.")
        if value and value.size > 10485760:
            raise serializers.ValidationError("Datei zu groß. Maximum: 10MB")
        return value


class EventSerializer(serializers.ModelSerializer):
    """
    Event-Modell
    Beinhaltet Validierung für Pflichtfelder
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
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Event-Name muss mindestens 3 Zeichen haben.")
        return value

    def validate_duration(self, value):
        if value <= 0:
            raise serializers.ValidationError("Dauer muss größer als 0 sein.")
        if value > 480:
            raise serializers.ValidationError("Event kann maximal 8 Stunden (480 Min) dauern.")
        return value

    def validate_date(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("Event-Datum muss in der Zukunft liegen.")
        return value

    def validate_img(self, value):
        if value and hasattr(value, 'size'):
            if value.size > 5242880:  # 5MB
                raise serializers.ValidationError("Bild zu groß. Maximum: 5MB")
        return value

    def validate(self, data):
        # Setze Host auf Benutzernamen falls nicht angegeben 
        if data.get('is_public', True) and not data.get('host'):
            data['host'] = self.context['request'].user.username
        return data


class SavedPitchSerializer(serializers.ModelSerializer):
    """
    SavedPitch-Modell
    Gibt vollständigen Pitch-Daten zusammen mit dem Speicherzeitpunkt zurück
    """
    pitch = PitchSerializer(read_only=True)
    user = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = SavedPitch
        fields = ['id', 'user', 'pitch', 'saved_at']
        read_only_fields = ['id', 'user', 'saved_at']


class InvestmentSerializer(serializers.ModelSerializer):
    """
    Investment-Modell
    Beinhaltet Pitch-Details und berechnete Felder
    """
    investor = serializers.CharField(source='investor.username', read_only=True)
    pitch = PitchSerializer(read_only=True)
    pitch_id = serializers.IntegerField(write_only=True, required=False)
    roi = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    current_value = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = Investment
        fields = [
            'id', 'investor', 'pitch', 'pitch_id',
            'amount', 'equity_percentage', 'investment_date', 'status',
            'exit_date', 'exit_amount', 'notes', 'roi', 'current_value',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'investor', 'investment_date', 'created_at', 'updated_at']

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Investment-Betrag muss größer als 0 sein.")
        return value

    def validate_equity_percentage(self, value):
        if value is not None and (value < 0 or value > 100):
            raise serializers.ValidationError("Equity-Anteil muss zwischen 0 und 100% liegen.")
        return value

