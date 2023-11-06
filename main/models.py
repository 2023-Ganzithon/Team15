from django.db import models


class Material(models.Model):
    material = models.CharField(max_length=100)


class WeeklyMaterial(models.Model):
    matId = models.ForeignKey('main.Material', on_delete=models.CASCADE)
    week = models.DateTimeField(auto_now_add=True)