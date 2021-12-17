from django.db import models
from django.conf import settings

from outlet.models import Campain
# Create your models here.

class KPI(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    start_day = models.DateField()
    volume_achieved = models.CharField(max_length=200)
    table_share = models.CharField(max_length=200)
    consumer_reached = models.CharField(max_length=200)
    conversion = models.CharField(max_length=200)
    campain = models.ForeignKey(Campain, on_delete=models.CASCADE, blank=True)
    created = models.DateField(auto_now_add=True)