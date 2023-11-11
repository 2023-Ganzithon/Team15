from django.urls import path
from challenge.views import challenge_home , challenge_upload,challenge_detail
app_name = "challenge"

urlpatterns = [
    path('', challenge_home, name = 'challenge_home'),
    path('upload/<int:Id>', challenge_upload, name = 'challenge_upload'),
    path('detail/<int:Id>', challenge_detail, name = 'challenge_detail'),
]