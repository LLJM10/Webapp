from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, BasePermission, IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.conf import settings

from .models import Todo, Pitch, Event, SavedPitch
from .serializers import TodoSerializer, PitchSerializer, EventSerializer, SavedPitchSerializer


@api_view(["GET"])
def hello(request):
    return Response({"message": "Hallo von Django!"})


class TodoViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer


class IsOwnerOrReadOnly(BasePermission):
    """
    Custom permission: only allow owner of an object to edit/delete it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request (GET, HEAD, OPTIONS)
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        # Write permissions are only allowed to the owner
        return obj.owner == request.user


class PitchViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Pitch model.
    - Anonymous users can list/read public pitches.
    - Authenticated users can create pitches (owner set automatically).
    - Only owner can update/delete their pitches.
    - ?mine=true filter returns only pitches of the authenticated user.
    """
    queryset = Pitch.objects.all()
    serializer_class = PitchSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def perform_create(self, serializer):
        """Set owner to the current user when creating a pitch."""
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        """
        Optionally filter queryset:
        - ?mine=true returns only user's own pitches (requires auth)
        - Otherwise returns public pitches (is_public=True) or all if staff
        """
        qs = super().get_queryset()
        
        # If user requests their own pitches
        if self.request.query_params.get('mine') in ['1', 'true', 'True']:
            if self.request.user.is_authenticated:
                return qs.filter(owner=self.request.user)
            else:
                return qs.none()  # Anonymous users have no pitches
        
        # For public listing (marketplace)
        if self.request.user.is_authenticated and self.request.user.is_staff:
            # Staff can see all pitches
            return qs
        else:
            # Public users see only public pitches
            return qs.filter(is_public=True)
        
        return qs


class EventViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Event model.
    - Anonymous users can list/read public events.
    - Authenticated users can create events (owner set automatically).
    - Only owner can update/delete their events.
    - ?mine=true filter returns only events of the authenticated user.
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        """Set owner to the current user when creating an event."""
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        """
        Optionally filter queryset:
        - ?mine=true returns only user's own events (requires auth)
        - Otherwise returns public events (is_public=True) or all if staff
        """
        qs = super().get_queryset()
        
        # If user requests their own events
        if self.request.query_params.get('mine') in ['1', 'true', 'True']:
            if self.request.user.is_authenticated:
                return qs.filter(owner=self.request.user)
            else:
                return qs.none()  # Anonymous users have no events
        
        # For public listing (marketplace)
        if self.request.user.is_authenticated and self.request.user.is_staff:
            # Staff can see all events
            return qs
        else:
            # Public users see only public events
            return qs.filter(is_public=True)
        
        return qs


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_ai_description(request):
    """
    Generate AI description using Groq API.
    Expects: { "type": "pitch"|"event", "keywords": "...", "tone": "professional"|"creative"|"technical" }
    Returns: { "description": "..." }
    """
    try:
        from groq import Groq
    except ImportError:
        return Response(
            {"error": "Groq package not installed. Run: pip install groq"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    # Get request data
    content_type = request.data.get('type', 'pitch')
    keywords = request.data.get('keywords', '')
    tone = request.data.get('tone', 'professional')
    
    if not keywords:
        return Response(
            {"error": "Keywords are required"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Check if API key is configured
    api_key = getattr(settings, 'GROQ_API_KEY', None)
    if not api_key:
        return Response(
            {"error": "GROQ_API_KEY not configured in settings"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    # Build prompt based on type and tone
    tone_map = {
        'professional': 'professionell und überzeugend',
        'creative': 'kreativ und einzigartig',
        'technical': 'technisch detailliert und präzise'
    }
    tone_desc = tone_map.get(tone, 'professionell')
    
    if content_type == 'event':
        prompt = f"""Schreibe eine ansprechende Event-Beschreibung auf Deutsch. 
Die Beschreibung soll {tone_desc} sein.
Stichworte: {keywords}

Schreibe 2-3 Sätze, die klar erklären worum es geht und warum Teilnehmer kommen sollten.
Antworte NUR mit der Beschreibung, ohne zusätzliche Kommentare."""
    else:  # pitch
        prompt = f"""Schreibe eine überzeugende Pitch-Beschreibung für ein Startup auf Deutsch.
Die Beschreibung soll {tone_desc} sein.
Stichworte: {keywords}

Schreibe 2-3 Sätze, die das Problem, die Lösung und den Mehrwert klar kommunizieren.
Antworte NUR mit der Beschreibung, ohne zusätzliche Kommentare."""
    
    try:
        # Call Groq API
        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "Du bist ein Experte für Marketing-Texte und Startup-Pitches. Du schreibst prägnante, überzeugende Beschreibungen."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=200
        )
        
        description = response.choices[0].message.content.strip()
        
        return Response({
            "description": description
        })
        
    except Exception as e:
        return Response(
            {"error": f"AI generation failed: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


class SavedPitchViewSet(viewsets.ModelViewSet):
    """
    ViewSet for SavedPitch model.
    - Only authenticated users can save/unsave pitches.
    - Users can only see their own saved pitches.
    - Custom actions: save_pitch, unsave_pitch, check_saved
    """
    serializer_class = SavedPitchSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return only saved pitches of the current user."""
        return SavedPitch.objects.filter(user=self.request.user).select_related('pitch', 'pitch__owner')

    @action(detail=False, methods=['post'])
    def save_pitch(self, request):
        """
        Save a pitch for the current user.
        Expects: { "pitch_id": 123 }
        Returns: SavedPitchSerializer data or error
        """
        pitch_id = request.data.get('pitch_id')
        
        if not pitch_id:
            return Response(
                {"error": "pitch_id is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            pitch = Pitch.objects.get(id=pitch_id)
        except Pitch.DoesNotExist:
            return Response(
                {"error": "Pitch not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Create or get existing saved pitch
        saved_pitch, created = SavedPitch.objects.get_or_create(
            user=request.user,
            pitch=pitch
        )
        
        serializer = self.get_serializer(saved_pitch)
        
        if created:
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def unsave_pitch(self, request):
        """
        Remove a saved pitch for the current user.
        Expects: { "pitch_id": 123 }
        Returns: success message or error
        """
        pitch_id = request.data.get('pitch_id')
        
        if not pitch_id:
            return Response(
                {"error": "pitch_id is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            saved_pitch = SavedPitch.objects.get(
                user=request.user,
                pitch_id=pitch_id
            )
            saved_pitch.delete()
            return Response(
                {"message": "Pitch removed from saved list"},
                status=status.HTTP_200_OK
            )
        except SavedPitch.DoesNotExist:
            return Response(
                {"error": "Saved pitch not found"},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=['get'])
    def check_saved(self, request):
        """
        Check if a pitch is saved by the current user.
        Query param: ?pitch_id=123
        Returns: { "saved": true/false }
        """
        pitch_id = request.query_params.get('pitch_id')
        
        if not pitch_id:
            return Response(
                {"error": "pitch_id query parameter is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        is_saved = SavedPitch.objects.filter(
            user=request.user,
            pitch_id=pitch_id
        ).exists()
        
        return Response({"saved": is_saved})
