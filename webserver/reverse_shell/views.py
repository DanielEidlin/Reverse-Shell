from django.views import View
from django.http import HttpResponse
from .models import Attacker, Victim
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
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
