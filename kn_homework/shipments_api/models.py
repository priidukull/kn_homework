from django.db import models


# Create your models here.
class Shipment(models.Model):
    sender = models.CharField(max_length=255)
    receiver = models.CharField(max_length=255)
    tracking_code = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
