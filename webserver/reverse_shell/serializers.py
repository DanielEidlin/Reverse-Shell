from .models import Attacker, Victim
from rest_framework import serializers


class AttackerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attacker
        fields = ['id', 'ip', 'port', 'computer_name', 'mac_address']


class VictimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Victim
        fields = ['id', 'ip', 'port', 'computer_name', 'mac_address', 'logged_in']
