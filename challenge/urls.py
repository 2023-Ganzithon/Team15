from django.urls import path
from challenge.views import challenge_home , challenge_upload,challenge_detail
app_name = "challenge"

urlpatterns = [
    path('', challenge_home,name = 'challenge_home'),
    path('upload/', challenge_upload, name = 'challenge_upload'),
    path('detail/<int:cId>', challenge_detail, name = 'challenge_detail'),
]