from django.views import View
from rest_framework import viewsets
from django.http import HttpResponse
from .models import Attacker, Victim
from .serializers import AttackerSerializer, VictimSerializer


class HomeViewSet(View):
    def get(self, request):
        return HttpResponse("Hello, world. You're at the ReverseShell's index.")


class AttackerViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing attackers.
    """
    queryset = Attacker.objects.all()
    serializer_class = AttackerSerializer


class VictimViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing victims.
    """
    queryset = Victim.objects.all()
    serializer_class = VictimSerializer
