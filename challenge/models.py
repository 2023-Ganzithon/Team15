from django.db import models

# Create your models here.

class OngoingChallenge(models.Model):
    cCheck = models.BooleanField(default=False) # True = 성공/False = 실패
    uCheck = models.BooleanField(default=False) # True = 유저 확인완료/False=유저 미확인
    cDate = models.DateTimeField(auto_now_add=True)
    cImage = models.ImageField(upload_to='',null=True)
    cId = models.ForeignKey('challenge.challenge', on_delete=models.CASCADE)
    userId = models.ForeignKey('user.CustomUser', on_delete=models.CASCADE)

    def __str__(self):
        return self.cId.cName


class challenge(models.Model):
    cName = models.CharField(max_length=100)

    def __str__(self):
        return self.cName