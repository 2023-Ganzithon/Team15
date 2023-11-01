from django.db import models


class Material(models.Model):
    material = models.CharField(max_length=100)
