from django.urls import path
from .views import signup_view,login_view,logout_view,test_view

app_name = "user"

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('test/',test_view, name='test'),
]