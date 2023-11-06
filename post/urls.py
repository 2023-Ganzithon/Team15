from django.urls import path

from post.views import post_list, post_filtered

app_name = "post"

urlpatterns = [
    path('', post_list, name='post_list'),
    path('postList/<str:category>/<str:status>', post_filtered, name='post_filtered'),
]