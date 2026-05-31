from django.urls import *
from .views import comment_create, comment_like, comment_delete, comment_update
app_name = 'comments'

urlpatterns = [
    path('create/<int:post_id>/', comment_create, name='comment_create'),
    path('<int:comment_id>/like/', comment_like, name='comment_like'),
    path('delete/<int:comment_id>/', comment_delete, name='comment_delete'),
    path('update/<int:comment_id>/', comment_update, name='comment_update'),
]