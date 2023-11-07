from django.urls import path

from main.views import *

app_name = "main"

urlpatterns = [
    path('', mainpage_view, name="main_page"),
    path('sort_like/', sort_like_view, name="sort_like"),
    path('sort_buy/', sort_buy_view, name="sort_buy"),
]