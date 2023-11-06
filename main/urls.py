from django.urls import path

from main.views import mainpage_view

app_name = "main"

urlpatterns = [
    path('', mainpage_view, name="main_page"),
]