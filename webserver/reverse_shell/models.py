from django.db import models


class Attacker(models.Model):
    ip = models.GenericIPAddressField()
    port = models.IntegerField()
    computer_name = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.computer_name + ' ' + self.ip + ' ' + self.port


class Victim(models.Model):
    ip = models.GenericIPAddressField()
    port = models.IntegerField()
    computer_name = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.computer_name + ' ' + self.ip + ' ' + self.port
