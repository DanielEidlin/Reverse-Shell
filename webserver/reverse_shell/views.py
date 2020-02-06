from django.views import View
from rest_framework import viewsets
from django.http import HttpResponse
from .models import Attacker, Victim
from rest_framework.response import Response
from rest_framework.decorators import action
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

    @action(detail=False, methods=['get'])
    def available_victims(self, request):
        """
        Returns all the logged in victims.
        :return: Serialized victims that are logged in.
        """
        available_victims = Victim.objects.filter(logged_in=True)
        serialized_victims = VictimSerializer(available_victims, many=True)
        return Response(serialized_victims.data)
