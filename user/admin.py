from django.contrib import admin

from user.models import CustomUser, Attendance

admin.site.register(CustomUser)
admin.site.register(Attendance)

