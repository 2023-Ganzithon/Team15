from django.contrib import admin

# Register your models here.

from challenge.models import OngoingChallenge,challenge

admin.site.register(OngoingChallenge)
admin.site.register(challenge)