from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import viewsets

from .models import Todo
from .serializers import TodoSerializer


@api_view(["GET"])
def hello(request):
    return Response({"message": "Hallo von Django!"})


class TodoViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
