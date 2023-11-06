from django.urls import path
from .views import *

app_name = 'mypage'

urlpatterns = [
    path('', mypage_view, name='mypage'),
    path('attendance/', attendance_view, name='attendance'),
    path('challenge/', challenge_view, name='challenge'),
    path('bookmark/', bookmark_view, name='bookmark'),
]