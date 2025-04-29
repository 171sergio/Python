from django.db import models
from django.utils import timezone

class Carro(models.Model):
    placa = models.CharField(max_length=10)
    entrada = models.DateTimeField(default=timezone.now)
    saida = models.DateTimeField(null=True, blank=True)
