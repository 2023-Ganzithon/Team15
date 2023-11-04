from django.db import models

# Create your models here.

class OngoingChallenge(models.Model):
    cCheck = models.BooleanField(default=False) # True = 성공/False = 실패
    cDate = models.DateTimeField(auto_now_add=True)
    cImage = models.ImageField(null=False)
    cId = models.ForeignKey('challenge.challenge', on_delete=models.CASCADE)
    userId = models.ForeignKey('user.CustomUser', on_delete=models.CASCADE)


class challenge(models.Model):
    cName = models.CharField(max_length=100)