from django.urls import path

from post.views import post_list_view, post_filtered_view, post_create_view

app_name = "post"

urlpatterns = [
    path('', post_list_view, name='post_list'),
    path('filtered/', post_filtered_view, name='post_filtered'),
    path('create/', post_create_view, name='post_create'),
]