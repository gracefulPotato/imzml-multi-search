from django.db import models

# Create your models here.
class MassAtCoordinate(models.Model):
    rounded_mz = models.FloatField()
    mz = models.FloatField()
    abundance = models.IntegerField()
    x_coordinate = models.IntegerField()
    y_coordinate = models.IntegerField()

class ModelFormWithFileField(models.Model):
    title = models.CharField(max_length=50)
    file = models.FileField()
