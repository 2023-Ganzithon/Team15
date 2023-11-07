from django.urls import path

from post.views import post_list_view, post_filtered_view, post_create_view, post_update_view, post_detail_view, \
    post_delete_view, comment_delete_view, comment_create_view, post_status_view, video_list_view

app_name = "post"

urlpatterns = [
    path('', post_list_view, name='post_list'),
    path('filtered/', post_filtered_view, name='post_filtered'),
    path('create/', post_create_view, name='post_create'),
    path('<int:postId>/', post_detail_view, name='post_detail'),
    path('update/<int:postId>/', post_update_view, name='post_update'),
    path('deletePost/<int:postId>/', post_delete_view, name='post_delete'),
    path('createComment/<int:postId>/', comment_create_view, name='comment_create'),
    path('deleteComment/<int:commentId>/', comment_delete_view, name='comment_delete'),
    path('status/<int:postId>/<str:status>/', post_status_view, name='post_status'),
    path('video/', video_list_view, name='vide_list')
]