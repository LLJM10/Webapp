from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, BasePermission

from .models import Todo, Pitch
from .serializers import TodoSerializer, PitchSerializer


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
